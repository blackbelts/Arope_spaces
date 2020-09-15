from odoo import models, tools, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import timedelta, datetime


class AropeCollection(models.Model):
    _name='collection.arope'
    # policy=fields.Many2one('policy.arope',string='Policy')
    policy_no = fields.Integer(string="Policy No", copy=True)
    product = fields.Char(string="Product", copy=True,)
    refer_no = fields.Char(string="Policy No", copy=True)
    pin=fields.Integer(string='PIN')
    cur_code = fields.Char("Cur-Code", copy=True)
    prem_date=fields.Date(string='prem Date')
    total_lc=fields.Float(string='Total LC')
    paid_lc=fields.Float(string='Paid LC')
    uncleare_lc=fields.Float(string='Uncleared LC')
    paid_date = fields.Date(string="Paid Date", copy=True, default=datetime.today())
    due_date = fields.Date(string="Due Date", copy=True, default=datetime.today())
    agent_code=fields.Char(string='Agent_code')
    prm_status = fields.Char('Prm-Status')
