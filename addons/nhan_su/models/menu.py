from odoo import models, fields, api


class Menu(models.Model):
    _name = 'menu'
    _description = 'Menu'

    menu = fields.Char(string="menu")
    dropdown_menu = fields.Selection([
        ('menu', 'Menu')
    ],string='DropDown')