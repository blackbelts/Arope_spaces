from odoo import models, tools, fields, api,exceptions
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import timedelta, datetime,date

class AropePolicy(models.Model):
    _name = "policy.arope"
    _rec_name='policy_num'
    policy_num = fields.Integer(string="Policy Number", copy=True)
    issue_date = fields.Date(string="Issue Date", copy=True, default=datetime.today())
    first_inception_date = fields.Date(string="First Inception", copy=True, default=datetime.today())
    inception_date = fields.Date(string="Incetion", copy=True, default=datetime.today())
    expiry_date = fields.Date(string="End To", default=datetime.today(), copy=True)
    net_premium= fields.Float(string="Net Premium", copy=True)
    charges= fields.Float(string="Charges", copy=True)
    policy_cost= fields.Float(string="policy_cost", copy=True)
    fixed_stamps= fields.Float(string="Fixed stamps", copy=True)
    tax = fields.Float(string="Fixed stamps", copy=True)
    totoal_premium= fields.Float(string="Total Premium", copy=True)
    cur_code = fields.Char("Cur-Code", copy=True)
    pin=fields.Integer(string='PIN')
    rec_type = fields.Char(string='Rec Type' ,copy=False)
    endorsement_no = fields.Integer(string="Endorsement No.")
    # is_endorsement = fields.Boolean(string="", default=False)
    policy_serno = fields.Integer(string="policy SerNo.")
    policy_seq = fields.Integer(string="policy Seq.")
    product = fields.Char(string="Product", copy=True, )
    # endorsement_date = fields.Date(string="Endorsement Date")
    # customer = fields.Char('Customer', copy=True)
    customer_pin = fields.Integer('Insured PIN', copy=True)
    agent_code = fields.Char('Agent Code', copy=True,)
    introdagt = fields.Char('Introdagt', copy=True,)














