from odoo import models, fields, api
from odoo.tools import date_utils
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "oferta de la propietat immobiliària"
    _order = "price desc"

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
    property_type_id = fields.Many2one(
        comodel_name='estate.property.type',
        related='property_id.property_type_id',
        string="Property Type", store=True)

    # computed fields / Inverse Function
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Deadline", compute="_compute_validity_date", inverse="_inverse_validity_date")

    # sql constraints
    _sql_constraints = [
        ('check_property_offer_price', 'CHECK(price > 0)',
         'An offer price must be strictly positive'),
    ]

    @api.depends("create_date", "validity")
    def _compute_validity_date(self):
        """
            date = None
            if record.create_date:
                date = record.create_date
            else:
                date = fields.date.today()
        """
        print('compute!')
        for record in self:
            date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = date_utils.add(date, days=record.validity)

    # aplica quan es guarda el registre a la bd
    def _inverse_validity_date(self):
        print('inverse!')
        for record in self:
            date = record.create_date.date() if record.create_date else fields.Date.today()
            test = (record.date_deadline - date).days
            print(test)
            record.validity = test

    # action methods
    def action_accept_offer(self):
        if not 'accepted' in self.property_id.offer_ids.mapped('state'):
            self.state = 'accepted'
            self.property_id.selling_price = self.price
            self.property_id.buyer_id = self.partner_id
            self.property_id.state = 'offer_accepted'
        else:
            raise UserError("Only 1 offer can be accepted!")
        return True

    def action_refuse_offer(self):
        if self.state == 'accepted':
            self.property_id.selling_price = 0
            self.property_id.buyer_id = None
        self.state = 'refused'
        if not 'accepted' in self.property_id.offer_ids.mapped('state'):
            self.property_id.state = 'offer_received'
        return True

    # CRUD
    @api.model
    def create(self, vals):
        property = self.env['estate.property'].browse(vals['property_id'])
        if property.state in ('offer_accepted', 'sold', 'canceled'):
            raise UserError(
                'It is not allowed to create offers if the property has an accepted offer, is sold or cancelled')
        if vals['price'] <= property.best_price:
            raise UserError(f'The offer must be higher than {
                            property.best_price}')
        property.state = 'offer_received'
        return super(EstatePropertyOffer, self).create(vals)
