from odoo import models, fields, api


class MucDoVB(models.Model):
    _name = 'muc_do_van_ban'
    _description = 'Mức độ văn bản'

    so_van_ban_den = fields.Many2one("van_ban_den", string="Văn bản đến")
    so_van_ban_di = fields.Many2one("van_ban_di", string="Văn bản đi")
    muc_do_vb =fields.Selection(
        [
            ("Hỏa tốc ", "Hỏa tốc "),
            ("Thượng khẩn ", "Thượng khẩn "),
            ("Khuẩn ", "Khuẩn ")
        ],
        string="Mức độ văn bản", default="Hỏa tốc"
    )