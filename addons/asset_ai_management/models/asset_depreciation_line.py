from odoo import models, fields, api, _

class AssetDepreciationLine(models.Model):
    _name = 'asset.depreciation.line'
    _description = 'Chi tiết khấu hao tài sản'
    _order = 'depreciation_date'

    asset_id = fields.Many2one('asset.asset', string="Tài sản", ondelete='cascade')
    depreciation_date = fields.Date(string="Ngày khấu hao", required=True)
    amount = fields.Float(string="Số tiền khấu hao", required=True)
    remaining_value = fields.Float(string="Giá trị còn lại")
    
    is_posted = fields.Boolean(string="Đã ghi sổ", default=False)
    move_id = fields.Many2one('account.move', string="Bút toán kế toán", readonly=True)

    def action_post_depreciation(self):
        """Tạo bút toán kế toán cho dòng khấu hao này"""
        for line in self:
            if line.is_posted:
                continue
            
            asset = line.asset_id
            # Kiểm tra cấu hình kế toán từ Danh mục
            if not asset.category_id or not asset.category_id.journal_id:
                continue

            move_vals = {
                'journal_id': asset.category_id.journal_id.id,
                'date': line.depreciation_date,
                'ref': _("Khấu hao tháng: %s") % asset.name,
                'line_ids': [
                    # Nợ Tài khoản Chi phí Khấu hao
                    (0, 0, {
                        'name': _("Khấu hao định kỳ %s") % asset.name,
                        'account_id': asset.category_id.expense_account_id.id,
                        'debit': line.amount,
                        'credit': 0.0,
                    }),
                    # Có Tài khoản Tài sản (Giảm giá trị)
                    (0, 0, {
                        'name': _("Giảm giá trị tài sản %s") % asset.name,
                        'account_id': asset.category_id.asset_account_id.id,
                        'debit': 0.0,
                        'credit': line.amount,
                    }),
                ],
            }
            move = self.env['account.move'].create(move_vals)
            move.action_post()
            line.write({'move_id': move.id, 'is_posted': True})
            
            # Cập nhật lại giá trị hiện tại của tài sản
            asset.current_value -= line.amount