from odoo import models, fields, api
from odoo.exceptions import ValidationError


class inhertResPartner(models.Model):
    _inherit = 'res.partner'
    broker=fields.Boolean(string='Broker')
    broker_id = fields.Char(string='Broker ID')
    national_id = fields.Char(string='National ID')
    com_reg = fields.Char(string='Commerical Register')
    pin = fields.Integer(string='PIN')
    fra_no = fields.Char(string='FRA No')
    expire_date = fields.Date(string='Expiration Date')







