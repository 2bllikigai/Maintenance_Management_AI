from odoo import models, fields, api


class MuonTra(models.Model):
    _name = 'muon_tra'
    _description = "Quản lý mượn trả tài sane"
    _rec_name = 'ma_tai_san'

    ma_tai_san = fields.Many2one('tai_san', string="Tài sản", required=True)
    ngay_muon_du_kien = fields.Date("Ngày muợn dự kiến")
    ngay_tra_du_kien = fields.Date("Ngày trả dự kiến")
    ngay_muon_thuc_te = fields.Date("Ngày muợn thực tế")
    ngay_tra_thuc_te = fields.Date("Ngày trả thực tế")
    trang_thai = fields.Selection([
        ('gia_han_them', 'Gia hạn thêm'),
        ('tra_luon', 'Trả luôn'),
        ('dang_muon', 'Đang mượn')
    ], string="Trạng thái", default='gia_han_them')
    
    nhan_vien_id = fields.Many2one("nhan_vien", string="Người mượn")
    nguoi_tra = fields.Char("Người trả")
    nguoi_kiem_duyet = fields.Char("Người kiểm duyệt")
    nguoi_xac_nhan = fields.Many2one("nhan_vien", string="Người xác nhận")