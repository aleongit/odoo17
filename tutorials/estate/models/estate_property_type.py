from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "tipus de propietat immobiliària"

    name = fields.Char(
        string="Name",
        required=True
    )
