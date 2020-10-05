from odoo import models, tools, fields, api,exceptions
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import timedelta, datetime,date

class AropeClaim(models.Model):
    _name="claim.arope"
    _rec_name='claimNo'
    policy_no = fields.Integer(string="Policy Number", copy=True,)
    # line_of_bussines = fields.Char(string='Line of business')
    product = fields.Char(string="Product", copy=True,)
    sub_journal = fields.Char('Sub-Journal', copy=True)
    claim_year = fields.Char(string="Claim Year", copy=True, )
    claimNo = fields.Integer(string="ClaimNo", copy=True, )
    claim_serNo = fields.Integer(string="Claimserno", copy=True, )
    date_declared= fields.Date(string="Date Declared", copy=True,)
    date_occured= fields.Date(string="Date Occured", copy=True,)
    claim_status= fields.Char(string="Claim Status", copy=True,)
    policy_serno = fields.Integer(string="policy SerNo.")
    cur_code = fields.Char("Cur-Code", copy=True)
    pin=fields.Integer(string='PIN')
    claim_eval=fields.Float(string='Claim eval')
    fees_eval=fields.Float(string='Fees eval')
    recoveryamt_eval=fields.Float(string='Recovery Amt')
    claim_paid=fields.Float(string='Claim Paid')
    agent_code=fields.Char(string='Agent_code')















