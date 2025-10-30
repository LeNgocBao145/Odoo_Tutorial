from odoo import fields, models, api
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate property"

    name = fields.Char(required=True, string="Title")

    description = fields.Text()

    postcode = fields.Char()

    date_availability = fields.Date(default=fields.Date.today() + relativedelta(months=3), copy=False, string="Available From")

    expected_price = fields.Float(required=True)

    selling_price = fields.Float(readonly=True, copy=False)

    bedrooms = fields.Integer(default=2)

    living_area = fields.Integer(string ='Living Area (sqm)')

    facades = fields.Integer()

    garage = fields.Boolean()

    garden = fields.Boolean()

    garden_area = fields.Integer(string='Garden Area (sqm)')


    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ], string='Garden Orientation')


    Status = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled'),
    ], string='Status', default='new')

    active = fields.Boolean(default=True)

    property_type_id = fields.Many2one('estate.property.type', string="Property Type")

    buyer_id = fields.Many2one('res.partner', string="Buyer")
    salesperson_id = fields.Many2one('res.users', string="Salesman", default=lambda self: self.env.user)

    tag_ids = fields.Many2many('estate.property.tag', string="Tags")

    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")

    best_price = fields.Float(string='Best Offer', compute='_compute_best_price')

    total_area = fields.Integer(string='Total Area (sqm)', compute='_compute_total_area')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0.0)