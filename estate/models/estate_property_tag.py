from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"

    name = fields.Char(required=True, string="Name")
    color = fields.Integer('Color')

    _sql_constraints = [
        ('unique_tag_name', 'unique(name)', 'Property tag name must be unique!')
    ]