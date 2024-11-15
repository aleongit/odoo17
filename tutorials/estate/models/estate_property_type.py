from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "tipus de propietat immobiliària"
    _order = "name"

    name = fields.Char(
        string="Name",
        required=True
    )
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer('Sequence', default=1, help="Used to order types")

    # sql constraints
    _sql_constraints = [
        ('check_property_type_name', 'UNIQUE(name)',
         'A property type name must be unique'),
    ]
