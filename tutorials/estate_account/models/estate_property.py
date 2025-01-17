from odoo import models, fields, api, Command, _
from odoo.tools import date_utils
from odoo.exceptions import UserError, ValidationError

import logging

_logger = logging.getLogger(__name__)


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    # move_type = fields.Selection(selection=[
    #     ('entry', 'Journal Entry'),
    #     ('out_invoice', 'Customer Invoice'),
    #     ('out_refund', 'Customer Credit Note'),
    #     ('in_invoice', 'Vendor Bill'),
    #     ('in_refund', 'Vendor Credit Note'),
    #     ('out_receipt', 'Sales Receipt'),
    #     ('in_receipt', 'Purchase Receipt'),
    # ], string='Type', required=True, store=True, index=True, readonly=True, tracking=True,
    # default="entry", change_default=True)

    # overwrite
    def action_set_sold(self):
        res = super(EstateProperty, self).action_set_sold()
        _logger.info(
            'Pass for action_set_sold in inherit estate.property model \
                in estate_account module ')
        # create invoice
        vals = {}
        vals['partner_id'] = self.buyer_id.id
        vals['move_type'] = 'out_invoice'
        vals['invoice_line_ids'] = [
                # create line #1
                Command.create({
                    'name': self.name,
                    'quantity': 1,
                    'price_unit': self.selling_price * 0.06
                }),
                 # create line #2
                Command.create({
                    'name': 'Administrative Fees',
                    'quantity': 1,
                    'price_unit': 100.00
                })
            ]
        self.env['account.move'].create(vals)
        return res
