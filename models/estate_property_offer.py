from odoo import fields, models, api
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offer"

    price = fields.Float()

    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], nocopy=True)

    partner_id = fields.Many2one('res.partner', string="Partner", required=True)

    property_id = fields.Many2one('estate.property', string="Property", required=True)

    validity = fields.Integer(string="Validity (days)", default=7, inverse='_inverse_validity')

    date_deadline = fields.Date(string="Deadline", compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = record.create_date + timedelta(days=record.validity)            

    def _inverse_date_deadline(self):
        for record in self:
            record.date_deadline = record.create_date - timedelta(days=record.validity)  

    @api.depends('date_deadline')
    def _inverse_validity(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date).days
    