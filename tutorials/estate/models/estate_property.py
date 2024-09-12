from odoo import models, fields


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "descripció del model propietat immobilària"

    name = fields.Char(
        required=True
    )
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date()
    expected_price = fields.Float(
        required=True
    )
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Type',
        selection=[('north', 'North'), ('south', 'South'),
                   ('east', 'East'), ('west', 'West')],
        help="Type is used to indicate one of the four main points of the compass"
    )
    # selection
    # specifies the possible values for this field.
    # It is given as either a list of pairs (value, label),
    # or a model method, or a method name.
