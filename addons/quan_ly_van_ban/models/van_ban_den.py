from odoo import models,fields,api
from datetime import date

class VanBanDen(models.Model):
    _name = 'van_ban_den'
    _description = 'Bảng chứa văn bản'

    ten_van_ban =fields.Char("Tên văn bản ",required=True)
    so_van_ban_den =fields.Char("Số văn bản đến", required=True)
    so_hieu = fields.Char("Số hiệu", required=True)
    nam_den = fields.Datetime("Năm", required= True)
    noi_gui = fields.Char("Nơi gửi", required=True)
