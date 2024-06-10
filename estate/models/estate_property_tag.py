from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Real Estate Property Tag'
    _order = 'name'

    name = fields.Char(required=True)
    color = fields.Integer()

    _sql_constraints = [
        ('check_unique_name', 'UNIQUE (name)', 'Tag name already exists!'),
    ]
