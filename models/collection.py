from odoo import models, tools, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import timedelta, datetime


class AropeCollection(models.Model):
    _name='collection.arope'
    policy=fields.Many2one('policy.arope',string='Policy')
    customer=fields.Many2one(related='policy.customer' ,store=True ,string='Customer')
    collect_date=fields.Date(string='Collected Date',related='policy.issue_date',store=True)
    net_premium=fields.Float(string='Net Premium',related='policy.net_premium',store=True)
    gross_premium=fields.Float(string='Gross Premium',related='policy.gross_premium',store=True)
    broker=fields.Many2one(related='policy.broker',string='Broker')
    state = fields.Selection([('outstanding', 'Outstanding'),
                               ('paid', 'Paid'),
                              ('canceled', 'Canceled')],
                             'State', required=True, default='outstanding')