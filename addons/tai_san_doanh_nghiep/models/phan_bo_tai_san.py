from odoo import models, fields, api


class PhanBoTaiSan(models.Model):
    _name = 'phan_bo_tai_san'
    _description = "Quản lý vị trí và phân bổ tài sản"
    _rec_name = 'ma_tai_san'

    ma_tai_san = fields.Many2one('tai_san', string="Tài sản", required=True)
    vi_tri = fields.Char("Vị trí", required=True)
    ngay_phan_bo = fields.Date("Ngày phân bổ", required=True)
    nhan_vien_id = fields.Many2one("nhan_vien", string="Người phân bố")

    @api.onchange('ma_tai_san')
    def _onchange_ma_tai_san(self):
        if self.ma_tai_san:
            self.vi_tri = f"Vị trí hiện tại của tài sản: {self.ma_tai_san.ten_tai_san}"