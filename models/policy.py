from odoo import models, tools, fields, api,exceptions
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import timedelta, datetime,date

class AropePolicy(models.Model):
    _name = "policy.arope"
    _rec_name='policy_num'
    policy_num = fields.Char(string="Policy Number", copy=True,required=True)
    issue_date = fields.Date(string="Issue Date", copy=True, default=datetime.today())
    start_date = fields.Date(string="Start From", copy=True, default=datetime.today())
    end_date = fields.Date(string="End To", default=datetime.today(), copy=True)
    term = fields.Char()
    total_sum_insured = fields.Float(digits=(12, 2), string='Total Sum Insured')
    net_premium= fields.Float(string="Net Premium", copy=True)
    c= fields.Float(string="Gross Premium", copy=True)
    currency_id = fields.Char("Currency", copy=True)
    policy_status = fields.Char(string='Status' ,copy=False)
    endorsement_no = fields.Char(string="Endorsement No.")
    endorsement_reason = fields.Text(string='Endorsement Reason')
    endorsement_type = fields.Char('Endorsement Typr')
    # is_endorsement = fields.Boolean(string="", default=False)
    renewal_no = fields.Char(string="Renewal No.")
    line_of_bussines = fields.Char(string='Line of business')
    product = fields.Char(string="Product", copy=True, )
    endorsement_date = fields.Date(string="Endorsement Date")
    customer = fields.Char('Customer', copy=True)
    customer_pin = fields.Integer('Customer PIN', copy=True)

    broker = fields.Char('Broker', copy=True,)
    broker_pin = fields.Integer('Broker PIN', copy=True,)
    agent_code = fields.Char('Agent Code', copy=True,)


    policy_type = fields.Char()
    is_renewal = fields.Boolean(string="Renewal")
    # index=fields.Date()
    # collection_ids=fields.One2many('collection.arope','policy','Collections')
    # risk_ids=fields.One2many('policy.risk','policy_risk_id',string='Risks')
    # check_item = fields.Char()
    # ins_type = fields.Selection([('Individual', 'Individual'),
    #                              ('Group', 'Group'), ],
    #                             'I&G', track_visibility='onchange', copy=True, default='Individual', required=True)


    # @api.onchange('line_of_bussines', 'ins_type')
    # def _compute_insured_policy(self):
    #     if self.ins_type == 'Group':
    #         self.check_item = 'Group'
    #     else:
    #         self.check_item = self.line_of_bussines.object
    # def testyy(self):
    #     # self.index=date(date.today().year, 1, 1)-relativedelta(years=1)
    #     date_last_year = date(date.today().year, 1, 1) - relativedelta(years=1)
    #     date_start = date(date.today().year, 1, 1)
    #     date3 = date_start
    #
    #     for i in range(6):
    #         total = 0.0
    #         for pol in self.env['policy.arope'].search(
    #                 [('start_date', '>=', date3),('start_date', '<=', date3+relativedelta(months=1))]):
    #             total += pol.gross_premium
    #         date3 = date3 + relativedelta(months=1)










