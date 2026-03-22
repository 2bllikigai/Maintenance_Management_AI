from odoo import models, fields, api


class TaiSan(models.Model):
    _name = 'tai_san'
    _description = "Danh mục tài sản"
    _rec_name = 'ten_tai_san'

    ma_tai_san = fields.Char("Mã tài sản", required=True)
    ten_tai_san = fields.Char("Tên tài sản", required=True)
    loai_tai_san = fields.Selection([
        ('vat_tu', 'Vật tư'),
        ('thiet_bi', 'Thiết bị'),
    ], string="Loại tài sản", required=True)
    gia_tri = fields.Float("Giá trị")
    ngay_mua = fields.Date("Ngày mua")
    tinh_trang = fields.Selection([
        ('moi', 'Mới'),
        ('da_su_dung', 'Đã sử dụng'),
        ('hong', 'Hỏng'),
    ], string="Tình trạng")
    vi_tri = fields.Char("Vị trí")
    anh = fields.Binary("Ảnh")
    ghi_nhan_danh_gia_tai_san = fields.One2many("ghi_nhan_danh_gia_tai_san", 
                                        inverse_name="ma_tai_san", 
                                        string="Kiểm kê tài sản")
    phan_bo_tai_san = fields.One2many("phan_bo_tai_san", 
                                        inverse_name="ma_tai_san", 
                                        string="Lịch sử vị trí")
    bao_tri_sua_chua = fields.One2many("bao_tri_sua_chua", 
                                        inverse_name="ma_tai_san", 
                                        string="Bảo trì sửa chữa")
    quan_ly_rui_ro = fields.One2many("quan_ly_rui_ro", 
                                        inverse_name="ma_tai_san", 
                                        string="Quản lý rủi ro")
    muon_tra = fields.One2many("muon_tra", 
                                        inverse_name="ma_tai_san", 
                                        string="Quản lý mượn trả")