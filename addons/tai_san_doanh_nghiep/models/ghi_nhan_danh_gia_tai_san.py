from odoo import models, fields, api


class GhiNhanDanhGiaTaiSan(models.Model):
    _name = 'ghi_nhan_danh_gia_tai_san'
    _description = "Ghi nhận và đánh giá tài sản"
    _rec_name = 'ma_tai_san'

    ma_tai_san = fields.Many2one('tai_san', string="Tài sản", required=True)
    ngay_ghi_nhan = fields.Date("Ngày ghi nhận", required=True)
    gia_tri_hien_tai = fields.Float("Giá trị hiện tại")
    khau_hao = fields.Float("Khấu hao")
    ghi_chu = fields.Text("Ghi chú")
    nhan_vien_id = fields.Many2one("nhan_vien", string="Người đánh giá")

    @api.onchange('ma_tai_san')
    def _onchange_ma_tai_san(self):
        if self.ma_tai_san:
            self.gia_tri_hien_tai = self.ma_tai_san.gia_tri