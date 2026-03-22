from odoo import models, fields

class Maintenance(models.Model):
    _name = 'asset.maintenance'
    _description = 'Maintenance History'

    asset_id = fields.Many2one(
        'asset.asset', 
        string="Asset", 
        required=True, 
        ondelete='cascade'
    )

    # Đổi tên từ 'date' thành 'maintenance_date' để khớp với XML của bạn
    maintenance_date = fields.Date(
        string="Maintenance Date", 
        required=True,
        default=fields.Date.context_today # Tự động lấy ngày hôm nay cho tiện
    )

    cost = fields.Float(
        string="Maintenance Cost"
    )

    maintenance_type = fields.Selection([
        ('repair', 'Sửa chữa'),
        ('inspection', 'Kiểm tra định kỳ'),
        ('replacement', 'Thay thế linh kiện')
    ], string="Type", default='inspection')

    condition_after = fields.Selection([
        ('good', 'Tốt'),
        ('normal', 'Bình thường'),
        ('bad', 'Kém')
    ], string="Condition After Maintenance", default='good')

    note = fields.Text(string="Note")