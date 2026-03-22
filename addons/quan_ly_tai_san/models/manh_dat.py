from odoo import models,fields,api
from datetime import date

class ManhDat(models.Model):
    _name = 'manh_dat'
    _description = 'Bảng chứa nhà ở'

    id_manh_dat = fields.Char("Mã ", required=True)
    dia_chi = fields.Char("Địa chỉ nhà", required=True)
    gia_thanh = fields.Char("Giá thành", required=True)
    ngay_mua = fields.Date("Ngày mua", required= True)
    dien_tich = fields.Char("Diện tích", required=True)
    loai_tinh_trang = fields.Selection(
        [
            ("Chính chủ", "Chính chủ"),
            ("Chưa hoàn thành sang tên", "Chưa hoàn thành sang tên")
        ],
        string="Tình trạng mảnh đất", default="Chính chủ"
    )
    id_nhan_vat = fields.Many2one("nhan_vat", string="Nhân vật")