from odoo import models, fields, api


class ThongKeTaiSan(models.Model):
    _name = 'thong_ke_tai_san'
    _description = "Thống kê tài sản"
    _rec_name = 'ma_tai_san'

    ma_tai_san = fields.Many2one('tai_san', string="Tài sản hiện có", store=True)
    ma_tai_san = fields.Many2one('muon_tra', string="Tài sản đang mượn", store=True)
    so_luong_tai_san = fields.Integer("Số lượng tài sản",compute='_compute_so_luong_tai_san',  store=True)
    so_luong_muon = fields.Integer("Số lượng đang mượn", compute='_compute_so_luong_muon', store=True)
    so_luong_thuc_te = fields.Integer("Số lượng thực tế", compute='_compute_so_luong_thuc_te', store=True)

    @api.depends('ma_tai_san')
    def _compute_so_luong_tai_san(self):
        for record in self:
            # Tính số lượng tài sản hiện có từ model 'tai_san'
            record.so_luong_tai_san = self.env['tai_san'].search_count([])

    @api.depends('ma_tai_san')
    def _compute_so_luong_muon(self):
        for record in self:
            # Tính số lượng tài sản đang được mượn
            record.so_luong_muon = self.env['muon_tra'].search_count([
                ('trang_thai', 'in', ['dang_muon', 'gia_han_them'])
            ])

    @api.depends('so_luong_tai_san', 'so_luong_muon')
    def _compute_so_luong_thuc_te(self):
        for record in self:
            record.so_luong_thuc_te = record.so_luong_tai_san - record.so_luong_muon