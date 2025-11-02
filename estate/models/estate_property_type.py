from odoo import fields, models, api

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"    
    _order = "sequence, name"

    sequence = fields.Integer('Sequence', default=1)
    name = fields.Char(required=True, string="Type")
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(compute="_compute_offer_count")
    property_ids = fields.One2many('estate.property', 'property_type_id')

    _sql_constraints = [
        ('unique_type_name', 'unique(name)', 'Property type name must be unique!')
    ]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
