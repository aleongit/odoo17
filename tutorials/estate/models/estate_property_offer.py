from odoo import models, fields


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "oferta de la propietat immobiliària"

    price = fields.Float()
    state = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False
    )

    # Many2one
    partner_id = fields.Many2one(
        comodel_name='res.partner', string="Partner", required=True)
    property_id = fields.Many2one(
        comodel_name='estate.property', required=True)
