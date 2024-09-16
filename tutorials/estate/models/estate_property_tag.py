from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "tag de propietat immobiliària"

    name = fields.Char(
        string="Name",
        required=True
    )