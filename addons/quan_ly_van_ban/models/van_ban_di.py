from odoo import models,fields,api
from datetime import date

class VanBanDi(models.Model):
    _name = 'van_ban_di'
    _description = 'Bảng chứa văn bản'

    so_hieu = fields.Char("Số hiệu", required=True)
    ten_van_ban = fields.Char("Điền văn bản", required=True)
    so_van_ban_di =fields.Char("Tên văn bản ",required=True)
    nam_di = fields.Datetime("Năm đi", required= True)
    noi_den = fields.Char("Nơi đến", required=True)
