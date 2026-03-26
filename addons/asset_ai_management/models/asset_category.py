from odoo import models, fields, api

class AssetCategory(models.Model):
    _name = 'asset.category'
    _description = 'Danh mục tài sản'

    name = fields.Char(string="Tên danh mục", required=True)
    
    # --- CẤU HÌNH TÀI CHÍNH (Đề tài 5) ---
    journal_id = fields.Many2one('account.journal', string="Sổ nhật ký", domain=[('type', '=', 'general')], required=True)
    asset_account_id = fields.Many2one('account.account', string="Tài khoản tài sản", required=True)
    expense_account_id = fields.Many2one('account.account', string="Tài khoản chi phí bảo trì", required=True)
    
    # --- QUY TẮC KHẤU HAO ---
    method_number = fields.Integer(string="Số tháng khấu hao", default=12, help="Tổng số tháng để tài sản hết giá trị")
    depreciation_method = fields.Selection([
        ('linear', 'Đường thẳng (Chia đều)'),
        ('degressive', 'Số dư giảm dần')
    ], string="Phương pháp khấu hao", default='linear')

    note = fields.Text(string="Ghi chú")