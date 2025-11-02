# from odoo import models, api, exceptions, Command

# class EstateAccount(models.Model):
#     _inherit = 'estate.property'

#     def action_sold(self, values):
#         self.ensure_one()

#         partner = self.partner_id or getattr(self, 'buyer_id', False)
#         if not partner:
#             raise exceptions.UserError("No partner specified on the property to create the invoice.")

#         values = {
#             'partner_id': partner.id,          
#             'move_type': 'out_invoice', 
#             "line_ids": [
#                 Command.create({
#                     "name": "value_1",
#                     "quantity": "value_2",
#                     "price_unit": "value_2",
#                 })
#             ],       
#         }

#         Journal = self.env['account.journal']
#         journal = Journal.search([], limit=1)
#         if journal:
#             values['journal_id'] = journal.id

#         self.env['account.move'].create(values)
#         return super(EstateAccount, self).action_sold(values)             
from odoo import models, exceptions, Command
from odoo.tools import float_round

class EstateAccount(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        self.ensure_one()

        partner = self.buyer_id
        if not partner:
            raise exceptions.UserError("No partner specified on the property to create the invoice.")

        Journal = self.env['account.journal']
        journal = Journal.search([('type', '=', 'sale')], limit=1) or Journal.search([], limit=1)
        if not journal:
            raise exceptions.UserError("No accounting journal found. Please configure an accounting journal.")

        # Tìm income account để gán cho invoice lines
        income_account = False
        # một số journal có trường income_account_id / default_account_id / default_credit_account_id
        for attr in ('default_account_id', 'income_account_id', 'default_credit_account_id', 'default_debit_account_id'):
            acct = getattr(journal, attr, False)
            if acct:
                income_account = acct.id
                break
        # fallback: tìm account theo loại user_type 'income'
        if not income_account:
            acc = self.env['account.account'].search([('user_type_id.type', '=', 'income')], limit=1)
            if acc:
                income_account = acc.id
        if not income_account:
            raise exceptions.UserError("No income account found for invoice lines. Please configure a journal with an income account or create an income account.")

        # Tính toán các giá trị dòng hoá đơn
        selling_price = float(self.selling_price or 0.0)
        commission_amount = float_round(0.06 * selling_price, precision_digits=2)
        admin_fee = 100.00

        # Chuẩn bị dict tạo invoice (dùng Command.create cho các dòng)
        invoice_vals = {
            'partner_id': partner.id,
            'move_type': 'out_invoice',    # Customer Invoice
            'journal_id': journal.id,
            'invoice_line_ids': [
                Command.create({
                    'name': f'Commission (6%) for property {self.name or ""}',
                    'quantity': 1.0,
                    'price_unit': commission_amount,
                    'account_id': income_account,
                }),
                Command.create({
                    'name': f'Administrative fees for property {self.name or ""}',
                    'quantity': 1.0,
                    'price_unit': admin_fee,
                    'account_id': income_account,
                }),
            ],
        }

        # Tạo invoice
        invoice = self.env['account.move'].create(invoice_vals)

        # Gọi super để giữ hành vi cha (ví dụ set trạng thái sold, các bước khác)
        return super(EstateAccount, self).action_sold()
