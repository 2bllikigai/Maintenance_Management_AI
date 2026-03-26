# models/asset_request.py
from odoo import models, fields, api, _

class AssetRequest(models.Model):
    _name = 'asset.request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Yêu cầu mua sắm tài sản'

    name = fields.Char(string="Mã yêu cầu", required=True, copy=False, readonly=True, default=lambda self: _('New'))
    asset_name = fields.Char(string="Tên tài sản cần mua", required=True, tracking=True)
    
    # --- KẾT NỐI NHÂN SỰ ---
    employee_id = fields.Many2one('hr.employee', string="Người yêu cầu", default=lambda self: self.env.user.employee_id, required=True)
    department_id = fields.Many2one('hr.department', related='employee_id.department_id', string="Phòng ban", readonly=True)

    # --- KẾT NỐI TÀI CHÍNH ---
    category_id = fields.Many2one('asset.category', string="Danh mục tài sản", required=True)
    estimated_cost = fields.Float(string="Kinh phí dự kiến", required=True, tracking=True)
    
    date_request = fields.Date(string="Ngày yêu cầu", default=fields.Date.today)
    reason = fields.Text(string="Lý do mua sắm")
    
    state = fields.Selection([
        ('draft', 'Nháp'),
        ('submitted', 'Chờ duyệt'),
        ('approved', 'Đã phê duyệt'),
        ('rejected', 'Từ chối'),
        ('purchased', 'Đã tạo tài sản')
    ], string="Trạng thái", default='draft', tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('asset.request') or _('New')
        return super(AssetRequest, self).create(vals)

    def action_submit(self):
        self.state = 'submitted'

    def action_approve(self):
        self.state = 'approved'

    def action_create_asset(self):
        """Chuyển yêu cầu thành tài sản"""
        for record in self:
            # SỬ DỤNG self.env ĐỂ GỌI MODEL KHÁC, KHÔNG DÙNG IMPORT
            asset_vals = {
                'name': record.asset_name,
                'category_id': record.category_id.id,
                'original_value': record.estimated_cost,
                'current_value': record.estimated_cost,
                'employee_id': record.employee_id.id,
                'maintenance_status': 'ready',
            }
            # Tạo bản ghi mới
            new_asset = self.env['asset.asset'].create(asset_vals)
            
            # Gọi hàm tính khấu hao từ model asset.asset
            if hasattr(new_asset, 'compute_depreciation_board'):
                new_asset.compute_depreciation_board()
            
            record.state = 'purchased'