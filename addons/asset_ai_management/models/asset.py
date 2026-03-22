from datetime import date
from odoo import models, fields, api
from ..ai.maintenance_predict import predict_next_maintenance
import logging

_logger = logging.getLogger(__name__)

class Asset(models.Model):
    _name = 'asset.asset'
    _description = 'Tài sản'

    name = fields.Char(string="Tên tài sản", required=True)
    original_value = fields.Float(string="Giá trị gốc")
    current_value = fields.Float(string="Giá trị hiện tại")
    employee_id = fields.Many2one('hr.employee', string="Nhân viên sử dụng")
    
    condition = fields.Selection([
        ('good', 'Tốt'),
        ('normal', 'Bình thường'),
        ('bad', 'Kém')
    ], string="Tình trạng", default='normal')

    maintenance_status = fields.Selection([
        ('ready', 'Sẵn sàng'),
        ('maintaining', 'Đang bảo trì'),
        ('broken', 'Đang hỏng'),
        ('waiting', 'Đang chờ linh kiện')
    ], string="Trạng thái bảo trì", default='ready')

    # Kết nối tới lịch sử bảo trì
    maintenance_ids = fields.One2many(
        'asset.maintenance',
        'asset_id',
        string="Lịch sử bảo trì"
    )

    # Dự báo AI (Lưu vào database để lọc/sắp xếp)
    predicted_next_maintenance = fields.Date(
        string="Ngày bảo trì dự kiến (AI)",
        compute="_compute_maintenance",
        store=True
    )

    # Cảnh báo (Không store để nó tự cập nhật theo ngày hiện tại)
    maintenance_warning = fields.Boolean(
        string="Cảnh báo bảo trì",
        compute="_compute_warning"
    )

    @api.depends('original_value', 'current_value', 'condition', 'maintenance_ids')
    def _compute_maintenance(self):
        """Hàm gọi AI để dự đoán"""
        for record in self:
            # Truyền record hiện tại và tập dữ liệu bảo trì vào hàm AI
            record.predicted_next_maintenance = predict_next_maintenance(
                record,
                record.maintenance_ids
            )

    @api.depends('predicted_next_maintenance')
    def _compute_warning(self):
        """Tính toán xem có hiện màu đỏ hay banner cảnh báo không"""
        today = date.today()
        for record in self:
            if record.predicted_next_maintenance:
                # Nếu ngày dự báo <= ngày hiện tại + 5 ngày thì hiện cảnh báo
                days_left = (record.predicted_next_maintenance - today).days
                record.maintenance_warning = days_left <= 5
            else:
                record.maintenance_warning = False

    @api.model
    def cron_predict_maintenance(self):
        """Hàm được gọi bởi Scheduled Action (Cron) hàng ngày"""
        _logger.info("Bắt đầu chạy Cron dự báo bảo trì AI...")
        assets = self.search([])
        for asset in assets:
            # Kích hoạt tính toán lại AI cho từng tài sản
            asset._compute_maintenance()
        _logger.info("Hoàn thành cập nhật dự báo cho %s tài sản.", len(assets))