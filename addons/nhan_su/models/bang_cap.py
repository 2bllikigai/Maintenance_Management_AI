from odoo import models, fields, api


class BangCap(models.Model):
    _name = 'bang_cap'
    _description = "Danh mục bằng cấp"
    _rec_name = 'ten_bang_cap'

    ma_bang_cap = fields.Char("Mã bằng cấp", required=True)
    ten_bang_cap = fields.Char("Tên bằng cấp", required=True)
    loai_bang_cap = fields.Char("Loại bằng cấp")