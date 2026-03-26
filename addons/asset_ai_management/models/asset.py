from datetime import date, timedelta
from odoo import models, fields, api, _
from ..ai.maintenance_predict import predict_next_maintenance
import logging

_logger = logging.getLogger(__name__)

class Asset(models.Model):
    _name = 'asset.asset'
    _inherit = ['mail.thread', 'mail.activity.mixin'] # Hỗ trợ Log và Chat bên dưới Form
    _description = 'Tài sản'

    name = fields.Char(string="Tên tài sản", required=True, tracking=True)
    
    # --- PHÂN LOẠI & KẾ TOÁN (Đề tài 5) ---
    category_id = fields.Many2one('asset.category', string="Danh mục tài sản", required=True, tracking=True)
    
    original_value = fields.Float(string="Giá trị gốc", tracking=True)
    current_value = fields.Float(string="Giá trị hiện tại", tracking=True)
    
    # Các trường kế toán lấy tự động từ danh mục
    journal_id = fields.Many2one('account.journal', string="Sổ nhật ký", domain=[('type', '=', 'general')])
    asset_account_id = fields.Many2one('account.account', string="Tài khoản tài sản")
    expense_account_id = fields.Many2one('account.account', string="Tài khoản chi phí bảo trì")

    # --- KẾT NỐI NHÂN SỰ (Yêu cầu bắt buộc) ---
    employee_id = fields.Many2one('hr.employee', string="Nhân viên sử dụng", help="Người giữ máy")
    technician_id = fields.Many2one('hr.employee', string="Kỹ thuật viên phụ trách", help="Người đi sửa máy")

    # --- TRẠNG THÁI VÀ TÌNH TRẠNG ---
    condition = fields.Selection([
        ('good', 'Tốt'),
        ('normal', 'Bình thường'),
        ('bad', 'Kém')
    ], string="Tình trạng", default='normal', tracking=True)

    maintenance_status = fields.Selection([
        ('ready', 'Sẵn sàng'),
        ('maintaining', 'Đang bảo trì'),
        ('broken', 'Đang hỏng'),
        ('waiting', 'Đang chờ linh kiện')
    ], string="Trạng thái bảo trì", default='ready', tracking=True)

    # --- CÁC BẢNG DỮ LIỆU LIÊN QUAN ---
    maintenance_ids = fields.One2many('asset.maintenance', 'asset_id', string="Lịch sử bảo trì")
    depreciation_line_ids = fields.One2many('asset.depreciation.line', 'asset_id', string="Kế hoạch khấu hao")

    # --- AI DỰ BÁO ---
    predicted_next_maintenance = fields.Date(
        string="Ngày bảo trì dự kiến (AI)",
        compute="_compute_maintenance",
        store=True,
        tracking=True
    )

    maintenance_warning = fields.Boolean(string="Cảnh báo bảo trì", compute="_compute_warning")

    # ==========================
    # LOGIC NGHIỆP VỤ & TỰ ĐỘNG HÓA
    # ==========================

    @api.onchange('category_id')
    def _onchange_category_id(self):
        """Tự động lấy thông tin tài chính từ Danh mục khi chọn"""
        if self.category_id:
            self.journal_id = self.category_id.journal_id
            self.asset_account_id = self.category_id.asset_account_id
            self.expense_account_id = self.category_id.expense_account_id

    def compute_depreciation_board(self):
        """Tạo bảng kế hoạch khấu hao hàng tháng"""
        for asset in self:
            asset.depreciation_line_ids.unlink() # Xóa dòng cũ
            if not asset.category_id or asset.category_id.method_number <= 0:
                continue

            # Công thức: Khấu hao tháng = Giá trị gốc / Tổng số tháng khấu hao
            dep_amount = asset.original_value / asset.category_id.method_number
            current_date = fields.Date.today()
            rem_value = asset.original_value

            lines = []
            for i in range(asset.category_id.method_number):
                rem_value -= dep_amount
                lines.append((0, 0, {
                    'depreciation_date': current_date + timedelta(days=30 * (i + 1)),
                    'amount': dep_amount,
                    'remaining_value': max(0, rem_value),
                }))
            asset.write({'depreciation_line_ids': lines})

    @api.depends('original_value', 'current_value', 'condition', 'maintenance_ids')
    def _compute_maintenance(self):
        """Hàm gọi AI dự đoán hỏng hóc"""
        for record in self:
            record.predicted_next_maintenance = predict_next_maintenance(
                record,
                record.maintenance_ids
            )

    @api.depends('predicted_next_maintenance', 'technician_id')
    def _compute_warning(self):
        """Cảnh báo và tự động giao việc cho nhân sự"""
        today = date.today()
        for record in self:
            if record.predicted_next_maintenance:
                days_left = (record.predicted_next_maintenance - today).days
                is_warning = days_left <= 5
                record.maintenance_warning = is_warning

                # TỰ ĐỘNG TẠO HOẠT ĐỘNG CHO KỸ THUẬT VIÊN
                if is_warning and record.technician_id and record.technician_id.user_id:
                    existing_activity = self.env['mail.activity'].search([
                        ('res_id', '=', record.id),
                        ('res_model', '=', 'asset.asset'),
                        ('summary', 'like', 'AI Cảnh báo')
                    ])
                    if not existing_activity:
                        record.activity_schedule(
                            'mail.mail_activity_data_todo',
                            summary=_("AI Cảnh báo: Bảo trì %s") % record.name,
                            note=_("Dự báo máy sắp hỏng trong %s ngày.") % days_left,
                            user_id=record.technician_id.user_id.id,
                            date_deadline=record.predicted_next_maintenance
                        )
            else:
                record.maintenance_warning = False

    # ==========================
    # HÀM CHẠY CRON (SCHEDULED ACTIONS)
    # ==========================

    @api.model
    def cron_predict_maintenance(self):
        """AI cập nhật dự báo hàng ngày"""
        _logger.info("Cron AI: Cập nhật dự báo bảo trì...")
        self.search([])._compute_maintenance()

    @api.model
    def cron_post_depreciation(self):
        """Kế toán: Tự động trích khấu hao hàng tháng"""
        _logger.info("Cron Kế toán: Bắt đầu trích khấu hao...")
        today = fields.Date.today()
        lines = self.env['asset.depreciation.line'].search([
            ('depreciation_date', '<=', today),
            ('is_posted', '=', False)
        ])
        for line in lines:
            try:
                line.action_post_depreciation()
            except Exception as e:
                _logger.error("Lỗi khấu hao dòng %s: %s", line.id, str(e))