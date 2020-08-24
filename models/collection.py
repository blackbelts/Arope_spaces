from odoo import models, tools, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import timedelta, datetime


class AropeCollection(models.Model):
    _name='collection.arope'
    # policy=fields.Many2one('policy.arope',string='Policy')
    policy_num = fields.Char(string="Policy Number", copy=True,required=True)
    customer=fields.Char(string='Customer')
    customer_pin=fields.Integer(string='Customer PIN')
    prem_date=fields.Date(string='prem Date')
    net_premium=fields.Float(string='Net Premium')
    gross_premium=fields.Float(string='Gross Premium')
    broker=fields.Char(string='Broker')
    broker_pin=fields.Integer(string='Broker PIN')
    agent_code=fields.Char(string='Agent_code')

    state = fields.Char('State')
    endorsement_no = fields.Char(string="Endorsement No.")
    endorsement_type = fields.Char(string="Endorsement Type.")