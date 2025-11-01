from odoo import fields, models, api, exceptions   
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offer"
    _order = "price desc"

    price = fields.Float()

    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], copy=False)

    partner_id = fields.Many2one('res.partner', string="Partner", required=True)

    property_id = fields.Many2one('estate.property', string="Property", required=True)

    validity = fields.Integer(string="Validity (days)", default=7)

    date_deadline = fields.Date(string="Deadline", compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    _sql_constraints = [
        ('check_price_positive', 'CHECK(price > 0)', 'The offer price must be strictly positive!'),
    ]

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)

    @api.depends('date_deadline')
    def _inverse_date_deadline(self):
        for record in self:
            if not record.date_deadline:
                record.date_deadline = record.create_date + timedelta(days=record.validity)
            else:
                record.validity = (record.date_deadline - record.create_date.date()).days

    def action_accept(self):
        for record in self: 
            offers = record.property_id.offer_ids.filtered(lambda o: o.status == 'accepted')
            if any(offer.status == 'accepted' for offer in offers):
                raise exceptions.UserError("Another offer has already been accepted for this property.")
            else:
                record.status = 'accepted'
                record.property_id.selling_price = record.price
                record.property_id.buyer_id = record.partner_id
                record.property_id.Status = 'offer_accepted'

    def action_refuse(self):
        for record in self: 
            record.status = 'refused'
            record.property_id.selling_price = 0
            record.property_id.buyer_id = False
    