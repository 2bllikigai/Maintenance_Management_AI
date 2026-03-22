from odoo import models, fields, api


class BaoTriSuaChua(models.Model):
    _name = 'bao_tri_sua_chua'
    _description = "Bảo trì và sửa chữa tài sản"
    _rec_name = 'ma_tai_san'

    ma_tai_san = fields.Many2one('tai_san', string="Tài sản", required=True)
    ngay_bao_tri = fields.Date("Ngày bảo trì", required=True)
    mo_ta = fields.Text("Mô tả công việc bảo trì/sửa chữa", required=True)
    chi_phi = fields.Float("Chi phí bảo trì/sửa chữa")
    nhan_vien_id = fields.Many2one("nhan_vien", string="Người thực hiện")
    trang_thai = fields.Selection([
        ('hoan_tat', 'Hoàn tất'),
        ('dang_thuc_hien', 'Đang thực hiện'),
        ('chua_thuc_hien', 'Chưa thực hiện'),
    ], string="Trạng thái", default='chua_thuc_hien')

    @api.onchange('ma_tai_san')
    def _onchange_ma_tai_san(self):
        if self.ma_tai_san:
            self.mo_ta = f"Bảo trì cho tài sản: {self.ma_tai_san.ten_tai_san}"