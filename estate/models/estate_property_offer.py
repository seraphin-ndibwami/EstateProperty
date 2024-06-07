from odoo import fields, models, api


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'

    price = fields.Float(required=True)
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], copy=False)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    property_type_id = fields.Many2one(
        'estate.property.type',
        related='property_id.property_type_id',
        store=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
    )

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            offer.date_deadline = fields.Date.add(offer.create_date, days=offer.validity) \
                if offer.create_date and offer.validity else False

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.create_date and offer.date_deadline:
                offer.validity = fields.Date.subtract(offer.date_deadline, offer.create_date).days()

