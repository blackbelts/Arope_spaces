from odoo import models, fields, api
from odoo.exceptions import ValidationError


class inhertResPartner(models.Model):
    _inherit = 'res.partner'
    broker=fields.Boolean(string='Broker')
    broker_id = fields.Char(string='Broker ID')



