from odoo import models, fields, api, _
from odoo.exceptions import UserError

class Maintenance(models.Model):
    _name = 'asset.maintenance'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Lịch sử bảo trì'
    _order = 'maintenance_date desc'

    asset_id = fields.Many2one(
        'asset.asset', 
        string="Tài sản", 
        required=True, 
        ondelete='cascade',
        tracking=True
    )

    maintenance_date = fields.Date(
        string="Ngày bảo trì", 
        required=True,
        default=fields.Date.context_today,
        tracking=True
    )

    # --- KẾT NỐI NHÂN SỰ (Mục II - Bắt buộc) ---
    technician_id = fields.Many2one(
        'hr.employee', 
        string="Người thực hiện", 
        required=True, # Nên để bắt buộc để đảm bảo tính kết nối nhân sự
        help="Nhân viên kỹ thuật trực tiếp sửa chữa",
        tracking=True
    )

    cost = fields.Float(string="Chi phí bảo trì", tracking=True)

    # --- AI ENHANCEMENT: MỨC ĐỘ HAO MÒN ---
    # Thêm trường này để AI tính toán "Wear Rate" (Tốc độ hao mòn)
    degradation_level = fields.Float(
        string="Mức độ hao mòn ghi nhận (%)", 
        help="Số liệu từ 0-100 để AI dự báo chính xác hơn",
        tracking=True
    )

    # --- QUẢN LÝ TRẠNG THÁI & KẾ TOÁN (Đề tài 5) ---
    state = fields.Selection([
        ('draft', 'Dự thảo'),
        ('done', 'Hoàn thành')
    ], string="Trạng thái", default='draft', tracking=True)

    move_id = fields.Many2one(
        'account.move', 
        string="Bút toán kế toán", 
        readonly=True,
        help="Liên kết tới sổ cái kế toán"
    )

    maintenance_type = fields.Selection([
        ('repair', 'Sửa chữa'),
        ('inspection', 'Kiểm tra định kỳ'),
        ('replacement', 'Thay thế linh kiện')
    ], string="Loại bảo trì", default='inspection')

    condition_after = fields.Selection([
        ('good', 'Tốt'),
        ('normal', 'Bình thường'),
        ('bad', 'Kém')
    ], string="Tình trạng sau bảo trì", default='good')

    note = fields.Text(string="Ghi chú")

    def action_done(self):
        """Xác nhận hoàn thành và hạch toán vào Kế toán"""
        for record in self:
            if record.state == 'done':
                raise UserError(_("Đơn bảo trì này đã hoàn thành rồi!"))
            
            asset = record.asset_id
            # Kiểm tra cấu hình kế toán từ Tài sản hoặc Danh mục
            if not asset.journal_id or not asset.expense_account_id or not asset.asset_account_id:
                raise UserError(_("Vui lòng cấu hình đầy đủ thông tin Kế toán trên Tài sản!"))

            if record.cost > 0:
                # TẠO BÚT TOÁN (JOURNAL ENTRY)
                move_vals = {
                    'journal_id': asset.journal_id.id,
                    'date': record.maintenance_date,
                    'ref': _("Bảo trì: %s") % asset.name,
                    'move_type': 'entry',
                    'line_ids': [
                        # Nợ Tài khoản Chi phí (Debit)
                        (0, 0, {
                            'name': _("Chi phí bảo trì %s") % asset.name,
                            'account_id': asset.expense_account_id.id,
                            'debit': record.cost,
                            'credit': 0.0,
                        }),
                        # Có Tài khoản Tài sản/Tiền (Credit)
                        (0, 0, {
                            'name': _("Thanh toán chi phí bảo trì %s") % asset.name,
                            'account_id': asset.asset_account_id.id,
                            'debit': 0.0,
                            'credit': record.cost,
                        }),
                    ],
                }
                move = self.env['account.move'].create(move_vals)
                move.action_post() # Ghi vào sổ cái
                record.move_id = move.id

            # Cập nhật thông tin ngược lại cho Tài sản sau bảo trì
            asset.write({
                'condition': record.condition_after,
                'maintenance_status': 'ready'
            })
            record.state = 'done'