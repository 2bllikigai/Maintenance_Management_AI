from odoo import models, fields, api


class QuanLyRuiRo(models.Model):
    _name = 'quan_ly_rui_ro'
    _description = "Quản lý rủi ro tài sản"
    _rec_name = 'ma_tai_san'

    ma_tai_san = fields.Many2one('tai_san', string="Tài sản", required=True)
    loai_rui_ro = fields.Selection([
        ('mat_mat', 'Mất mát'),
        ('hu_hong', 'Hư hỏng'),
        ('khong_dat', 'Không đạt yêu cầu'),
    ], string="Loại rủi ro", required=True)
    mo_ta = fields.Text("Mô tả rủi ro", required=True)
    ngay_xay_ra = fields.Date("Ngày xảy ra", required=True)
    nguoi_phu_trach = fields.Char("Người phụ trách", required=True)
    trang_thai = fields.Selection([
        ('da_giai_quyet', 'Đã giải quyết'),
        ('chua_giai_quyet', 'Chưa giải quyết'),
    ], string="Trạng thái", default='chua_giai_quyet')

    @api.onchange('ma_tai_san')
    def _onchange_ma_tai_san(self):
        if self.ma_tai_san:
            self.mo_ta = f"Rủi ro liên quan đến tài sản: {self.ma_tai_san.ten_tai_san}"