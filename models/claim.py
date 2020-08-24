from odoo import models, tools, fields, api,exceptions
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import timedelta, datetime,date



class AropeClaim(models.Model):
    _name="claim.arope"

    policy_num = fields.Char(string="Policy Number", copy=True,)
    line_of_bussines = fields.Char(string='Line of business')
    product = fields.Char(string="Product", copy=True,)

    customer = fields.Char('Customer', copy=True)
    customer_pin = fields.Char('Customer PIN', copy=True)
    broker = fields.Char('Broker', copy=True, )
    broker_pin = fields.Integer('Broker PIN', copy=True, )
    agent_code = fields.Char('Agent Code', copy=True, )
    endorsement_no = fields.Char(string="Endorsement No.")
    claim_num = fields.Char(string="Claim Number", copy=True, )
    intimation_num = fields.Char(string="Intimation Number", copy=True, )
    intimation_date= fields.Date(string="Intimation date", copy=True,)
    status = fields.Char(string="Status", copy=True, )
    paid_amount = fields.Char(string="Paid", copy=True, )


