from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "tipus de propietat immobiliària"
    _order = "name"

    name = fields.Char(
        string="Name",
        required=True
    )
    sequence = fields.Integer('Sequence', default=1,
                              help="Used to order types")
    # One2many
    property_ids = fields.One2many('estate.property', 'property_type_id')
    offer_ids = fields.One2many(
        comodel_name='estate.property.offer',
        inverse_name='property_type_id')

    offer_count = fields.Integer(
        string='Offer Count', compute='_compute_offer_count')

    # sql constraints
    _sql_constraints = [
        ('check_property_type_name', 'UNIQUE(name)',
         'A property type name must be unique'),
    ]

    # computed fields
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    # actions
    def action_view_offers(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Offers',
            'res_model': 'estate.property.offer',
            'view_mode': 'tree,form',
            'domain': [('property_type_id', '=', self.id)],
        }
