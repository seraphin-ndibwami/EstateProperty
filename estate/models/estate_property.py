from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'

    def _in_three_months(self):
        return fields.Date.add(fields.Date.context_today(self), months=3)

    def _current_user(self):
        return self.env.user

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=_in_three_months)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ])
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled')
    ], default='new')
    property_type_id = fields.Many2one('estate.property.type')
    buyer_id = fields.Many2one('res.partner', copy=False)
    salesperson_id = fields.Many2one('res.users', default=_current_user)
    offers_ids = fields.One2many('estate.property.offer', 'property_id')
    tag_ids = fields.Many2many('estate.property.tag')

    total_area = fields.Integer(compute='_compute_total_area')
    best_price = fields.Float(compute='_compute_best_price')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for each_property in self:
            each_property.total_area = each_property.living_area + each_property.garden_area

    @api.depends('offers_ids.price')
    def _compute_best_price(self):
        for each_property in self:
            return max(each_property.offers_ids.mapped('price') or [0])

    @api.onchange('garden')
    def _onchange_garden(self):
        self.ensure_one()
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.onchange('date_availability')
    def _onchange_date_availability(self):
        self.ensure_one()
        if self.date_availability and self.date_availability < fields.date.today():
            return {
                "warning": {
                    "title": _("Warning"),
                    "message": _("This availability date ( %s ) is in the past." % self.date_availability)
                }
            }

    def action_set_sold_property(self):
        self.ensure_one()
        if self.state == "canceled":
            raise UserError("You cannot set a canceled property to sold")

        self.state = 'sold'
        return True

    def action_set_canceled_property(self):
        self.ensure_one()
        if self.state == "sold":
            raise UserError("You cannot set a sold property to canceled")

        self.state = 'canceled'
        return True

    _sql_constraints = [
        ("check_expected_price", "CHECK(expected_price > 0)", "The expected price must be positive"),
        ("check_selling_price", "CHECK(selling_price IS NULL OR selling_price > 0)",
            "The selling price must be positive"),
    ]

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        """
        The selling price cannot be lower than 90% of the expected price
        """
        self.ensure_one()
        if self.selling_price and self.selling_price < self.expected_price * 0.9:
            self.selling_price = 0
            self.buyer_id = False
            raise ValidationError(
                _(f"The selling price {self.selling_price} $ of {self.name} cannot be lower than 90% \
                  of the expected price ({self.expected_price} $)"))
