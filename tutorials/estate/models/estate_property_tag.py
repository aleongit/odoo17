from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "tag de propietat immobiliària"
    _order = "name"

    name = fields.Char(
        string="Name",
        required=True
    )
    color = fields.Integer(string='Color')

    # sql constraints
    _sql_constraints = [
        ('check_property_tag_name', 'UNIQUE(name)',
         'A property tag name must be unique'),
    ]
