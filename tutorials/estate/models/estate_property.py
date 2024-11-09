from odoo import models, fields, api, _
from odoo.tools import date_utils
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "descripció del model propietat immobilària"
    _order = "id desc"

    # reserved fields (name, active, state)
    name = fields.Char(
        string="Name",
        required=True
    )
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(
        string='State',
        selection=[('new', 'New'),
                   ('offer_received', 'Offer Received'),
                   ('offer_accepted', 'Offer Accepted'),
                   ('sold', 'Sold '),
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
    # Selection [(value, label)]
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'),
                   ('east', 'East'), ('west', 'West')],
        help="Type is used to indicate one of the four main points of the compass"
    )

    # many2one
    property_type_id = fields.Many2one(
        "estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one(
        'res.users', string='Salesperson', index=True, default=lambda self: self.env.user)

    # many2many
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")

    # one2many
    offer_ids = fields.One2many(
        comodel_name="estate.property.offer", inverse_name="property_id")

    # computed fields
    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    # sql constraints
    _sql_constraints = [
        ('check_property_expected_price', 'CHECK(expected_price > 0)',
         'A property expected price must be strictly positive'),
        ('check_property_selling_price', 'CHECK(selling_price >= 0)',
         'A property selling price must be positive')
    ]

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0

    # onchange
    @api.onchange('garden')
    def onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
            return {'warning': {
                'title': _("Warning"),
                'message': ("garden it's True")}}
        else:
            self.garden_area = None
            self.garden_orientation = None
            return {'warning': {
                'title': _("Warning"),
                'message': ("garden it's False")}}

    # action methods
    def action_set_sold(self):
        if self.state != 'canceled':
            self.state = 'sold'
            # record.write({"state": "sold"})
        else:
            raise UserError("Canceled properties cannot be sold!")
        return True

    def action_set_canceled(self):
        if self.state != 'sold':
            self.state = 'canceled'
            # record.write({"state": "sold"})
        else:
            raise UserError("Sold properties cannot be canceled!")
        return True

    """
        def action_sold(self):
        if "canceled" in self.mapped("state"):
            raise UserError("Canceled properties cannot be sold.")
        return self.write({"state": "sold"})
    """

    # python constraint
    @api.constrains('selling_price')
    def _check_selling_price_is_expected(self):
        PER_CENT_EXPECTED = 0.90
        for record in self:
            expected_price_min = record.expected_price * PER_CENT_EXPECTED
            if record.selling_price < expected_price_min and record.selling_price > 0:
                raise ValidationError(f"The selling price must be at least {PER_CENT_EXPECTED:.2%} of the expected price!")
        # all records passed the test, don't return anything
