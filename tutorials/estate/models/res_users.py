from odoo import fields, models


class ResUsers(models.Model):

    _inherit = 'res.users'

    # one2many
    property_ids = fields.One2many(
        comodel_name='estate.property', inverse_name='salesperson_id',
        domain=[('state', 'in', ['new', 'offer_received'])])
