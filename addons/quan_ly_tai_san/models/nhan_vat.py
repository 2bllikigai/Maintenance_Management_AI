from odoo import models,fields,api
from datetime import date

class NhanVat(models.Model):
    _name = 'nhan_vat'
    _description = 'Bảng chứa người thụ hưởng tài sản'

    id_nhan_vat = fields.Char("Mã ", required=True)
    ho_va_ten = fields.Char("Họ và tên", required=True)
    so_dien_thoai =fields.Char("Số điện thoại",required=True)
    nam_sinh = fields.Datetime("Ngày tháng năm sinh", required= True)
    dia_chi = fields.Char("Địa chỉ", required=True)
    phuong_tien = fields.One2many("phuong_tien", 
                                        inverse_name="id_nhan_vat", 
                                        string="Danh sách xe")
    nha_o = fields.One2many("nha_o", 
                                        inverse_name="id_nhan_vat", 
                                        string="Danh sách tình trạng nhà")
    manh_dat = fields.One2many("manh_dat", 
                                        inverse_name="id_nhan_vat", 
                                        string="Danh sách tình trạng mảnh đất")
    tuoi = fields.Integer("Tuổi", compute="_compute_tinh_tuoi", stoge=True)
    anh = fields.Binary("Ảnh")

    @api.depends("nam_sinh")
    def _compute_tinh_tuoi(self):
        today = date.today()
        for record in self:
            if record.ngay_sinh:
                birth_date = fields.Date.from_string(record.ngay_sinh)
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                record.tuoi = age
            else:
                record.tuoi = 0  # or None if you prefer