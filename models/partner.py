from odoo import models, fields, api
from odoo.exceptions import ValidationError


class inhertResPartner(models.Model):
    _inherit = 'res.partner'
    national_id = fields.Char(string='National ID')
    com_reg = fields.Char(string='Commerical Register')
    pin = fields.Integer(string='PIN')
    fra_no = fields.Char(string='FRA No')
    expire_date = fields.Date(string='Expiration Date')
class inhertResUser(models.Model):
    _inherit = 'res.users'
    is_broker = fields.Boolean(string='Broker',default=True)
    agent_code = fields.Integer(string='Agent Code')
class InheritBrokers(models.Model):
    _name = 'table.b'
    _rec_name='name'
    name=fields.Char(string='Broker Name')
    card_id = fields.Char(string='Card ID')
    com_reg = fields.Integer(string='Commerical Register')
    pin = fields.Integer(string='PIN')
    fra_no = fields.Char(string='FRA No')
    expire_date = fields.Date(string='Expiration Date')
    agent_code = fields.Char(string='Agent Code')
    mobile = fields.Char(string='Mobile')









