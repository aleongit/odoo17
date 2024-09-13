from odoo import models, fields
from odoo.tools import date_utils


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "descripció del model propietat immobilària"

    # reserved fields (name, active, state)
    name = fields.Char(
        string="Name",
        required=True
    )
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(
        string='Status',
        selection=[('new', 'New'), ('offer_received', 'Offer Received'),
                   ('offer_accepted', 'Offer Accepted'), ('sold ', 'Sold '),
                   ('canceled', 'Canceled')],
        required=True,
        copy=False,
        default="new"
    )
    description = fields.Text(
        string="Description",
    )
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=date_utils.add(fields.date.today(), months=3)
    )
    expected_price = fields.Float(
        required=True
    )
    selling_price = fields.Float(
        readonly=True,
        copy=False
    )
    bedrooms = fields.Integer(
        default=2
    )
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'),
                   ('east', 'East'), ('west', 'West')],
        help="Type is used to indicate one of the four main points of the compass"
    )
    # selection
    # specifies the possible values for this field.
    # It is given as either a list of pairs (value, label),
    # or a model method, or a method name.
