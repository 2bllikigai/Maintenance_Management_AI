from odoo import models,fields,api
from datetime import date

class NhaO(models.Model):
    _name = 'nha_o'
    _description = 'Bảng chứa nhà ở'

    id_nha_o = fields.Char("Mã ", required=True)
    dia_chi = fields.Char("Địa chỉ nhà", required=True)
    gia_thanh = fields.Char("Giá thành", required=True)
    ngay_mua = fields.Date("Ngày mua", required= True)
    loai_tinh_trang = fields.Selection(
        [
            ("Trả góp", "Trả góp"),
            ("Hoàn thành mua nhà", "Hoàn thành mua nhà")
        ],
        string="Tình trạng nhà", default="Trả góp"
    )
    id_nhan_vat = fields.Many2one("nhan_vat", string="Nhân vật")