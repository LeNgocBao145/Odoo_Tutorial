from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char(required=True, string="Type")

    _sql_constraints = [
        ('unique_type_name', 'unique(name)', 'Property type name must be unique!')
    ]