from odoo import models, fields, api


class QuanLyBangCap(models.Model):
    _name = 'quan_ly_bang_cap'
    _description = 'Bảng chứa bằng cấp'

    khac = fields.Char("Khác")
    bang_cap_id = fields.Many2one("bang_cap", string="Bằng cấp")
    
    nhan_vien_id = fields.Many2one("nhan_vien", string="Nhân viên")