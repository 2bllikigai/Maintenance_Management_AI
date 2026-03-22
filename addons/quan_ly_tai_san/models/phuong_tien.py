from odoo import models,fields,api
from datetime import date

class PhuongTien(models.Model):
    _name = 'phuong_tien'
    _description = 'Bảng chứa phương tiện'

    id_phuong_tien = fields.Char("Mã ", required=True)
    ten_xe = fields.Char("Tên xe", required=True)
    noi_mua =fields.Char("Nơi mua",required=True)
    gia_thanh = fields.Char("Giá thành", required=True)
    ngay_mua = fields.Datetime("Ngày mua", required= True)
    loai_phuong_tien = fields.Selection(
        [
            ("Xe máy", "Xe máy"),
            ("Xe đạp", "Xe đạp"),
            ("Ô tô","Ô tô")
        ],
        string="Loại phương tiện", default="Xe máy"
    )
    id_nhan_vat = fields.Many2one("nhan_vat", string="Nhân vật")
    hang_xe = fields.Selection(
        [
            ("honda", "Honda"),
            ("yamaha", "Yamaha"),
            ("suzuki", "Suzuki"),
            ("khác", "Khác")
        ],
        string="Hãng xe",
        default=False
    )
    hang_xe_dap = fields.Selection(
        [
            ("trek", "Trek"),
            ("giant", "Giant"),
            ("specialized", "Specialized"),
            ("khac", "Khác")
        ],
        string="Hãng xe đạp",
        default=False
    )
    hang_xe_o_to = fields.Selection(
        [
            ("toyota", "Toyota"),
            ("ford", "Ford"),
            ("honda", "Honda"),
            ("khac", "Khác")
        ],
        string="Hãng ô tô",
        default=False
    )

    @api.onchange('loai_phuong_tien')
    def _onchange_loai_phuong_tien(self):
        if self.loai_phuong_tien == 'xe máy':
            self.hang_xe_dap = False  # Clear bike brand selection
            self.hang_xe_o_to = False  # Clear car brand selection
            return {'domain': {'hang_xe': [('id', '!=', False)], 'hang_xe_dap': [], 'hang_xe_o_to': []}}
        elif self.loai_phuong_tien == 'xe đạp':
            self.hang_xe = False  # Clear motorcycle brand selection
            self.hang_xe_o_to = False  # Clear car brand selection
            return {'domain': {'hang_xe_dap': [('id', '!=', False)], 'hang_xe': [], 'hang_xe_o_to': []}}
        elif self.loai_phuong_tien == 'ô tô':
            self.hang_xe = False  # Clear motorcycle brand selection
            self.hang_xe_dap = False  # Clear bike brand selection
            return {'domain': {'hang_xe_o_to': [('id', '!=', False)], 'hang_xe': [], 'hang_xe_dap': []}}
        else:
            self.hang_xe = False  # Clear motorcycle brand
            self.hang_xe_dap = False  # Clear bike brand
            self.hang_xe_o_to = False  # Clear car brand
            return {'domain': {'hang_xe': [], 'hang_xe_dap': [], 'hang_xe_o_to': []}}  # Clear domains