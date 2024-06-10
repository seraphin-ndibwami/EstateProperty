from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Real Estate Property Type'
    _order = 'name'

    name = fields.Char(required=True)
    _sql_constraints = [(
        'check_unique_name',
        'UNIQUE(name)',
        'this name already exists!')
    ]
    sequence = fields.Integer(default=1)
    property_ids = fields.One2many(
        'estate.property',
        'property_type_id',
        string='Properties'
    )

    offer_ids = fields.One2many(
        'estate.property.offer',
        'property_type_id',
        string='Offers'
    )
    offer_count = fields.Integer(
        compute='_compute_offer_count',
        store=True
    )

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for offer in self:
            offer.offer_count = len(offer.offer_ids)
