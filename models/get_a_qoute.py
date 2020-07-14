from datetime import timedelta, datetime
import base64
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo import api, fields, models,exceptions
import  math


class TravelQuotation(models.Model):
    _name = 'travel.quotation'
    _description = 'Get A Quote'

    package = fields.Selection([('individual', 'Individual'), ('family', 'Family')], 'Package For', default='individual')
    state = fields.Selection([('step_1', 'Quote Info'),
                              ('step_2', 'Price'),
                              ('step_3', 'Pay'), ],
                             'Steps', required=True, default='step_1', copy=False)
    geographical_coverage = fields.Selection([('zone 1', 'Europe'),
                                              ('zone 2', 'Worldwide excluding USA & CANADA'),
                                              ('zone 3', 'Worldwide'), ],
                                             'Zone',
                                             default='zone 1')
    DOB = fields.Date('Date Of Birth', default=datetime.today(), required=True)
    age = fields.Integer('Age', compute='compute_age',store=True)
    coverage_from = fields.Date('From', default=datetime.today(), required=True)
    coverage_to = fields.Date('To')
    days = fields.Integer('Day(s)',compute='compute_days',store='True', required=True)
    currency_id = fields.Many2one("res.currency", "Currency", copy=True,
                                  default=lambda self: self.env.user.company_id.currency_id, readonly=True)
    net_premium = fields.Float('Net Premium', readonly=True)
    proportional_stamp = fields.Float('Proportional Stamp', readonly=True)
    dimensional_stamp = fields.Float('Dimensional Stamp', readonly=True)
    supervisory_stamp = fields.Float('Supervisory Stamp', readonly=True)
    policy_approval_fees = fields.Float('Policy approval fees', readonly=True)
    policy_holder_fees = fields.Float('Policyholder’s protection fees', readonly=True)
    admin_fees = fields.Float('Admin Fees', readonly=True)

    issue_fees = fields.Float('Issue Fees', readonly=True)
    gross_premium = fields.Float('Gross Premium', readonly=True)
    issue_date = fields.Datetime(string='Issue Date', readonly=True, default=lambda self:fields.datetime.today())
    insured = fields.Char('Traveller Name')
    phone = fields.Char('Traveller Phone')
    address = fields.Char('Traveller Address')
    passport_num = fields.Char('Passport Number')
    national_id = fields.Char('National ID')
    gender = fields.Selection([('M', 'Male'), ('F', 'Female')])

    @api.depends('coverage_from', 'coverage_to')
    def compute_days(self):
        if self.coverage_from and self.coverage_to:
            # date1 = datetime.strptime(self.coverage_from, '%Y-%m-%d').date()
            # date2 = datetime.strptime(self.coverage_to, '%Y-%m-%d').date()
            date3 = (self.coverage_to - self.coverage_from).days
            self.days = date3
    @api.depends('DOB')
    def compute_age(self):
        if self.DOB:
            # date1 = datetime.strptime(str(self.issue_date), '%Y-%m-%d %H:%M:%S').date()
            # date2 = datetime.strptime(str(self.DOB), '%Y-%m-%d' ).date()
            difference = relativedelta(self.issue_date, self.DOB)
            age = difference.years
            months = difference.months
            days = difference.days
            if months or days != 0:
                age += 1
            self.age = age
    
    def edit_data(self):
        print('450450540')
        self.state = 'step_1'

    def go_to_traveller_info(self):   
        self.state = 'step_3'

    def get_financial_data(self):
        print('yessssssssssssssssssssssssssss')
        if self.age and self.geographical_coverage and self.days:
            print('ifffffffffffffff11111111111')
            if self.package == 'individual':
                    print('ifffffffffffffff2222222')
                    result=self.get_individual({'z':self.geographical_coverage,'d':[self.DOB],'p_from':self.coverage_from,'p_to':self.coverage_to})
            else:
                print('545454515748548541515')
                raise UserError((
                    "First Else"))

            if result:
                print('yessssssssssssssssssssssssssss')
                self.net_premium =  result.get('net')
                self.proportional_stamp = result.get('pro_stamp')
                self.dimensional_stamp = result.get('dimensional_stamp')
                self.supervisory_stamp = result.get('supervisory_stamp')
                self.policy_approval_fees = result.get('policy_approval_fees')
                self.policy_holder_fees = result.get('policy_holder_fees')
                self.issue_fees = result.get('issue_fees')
                self.gross_premium = result.get('gross')+self.admin_fees
                self.state = 'step_2'
                print('15151515151515')
                print(self.state)
            else:
                print('545454515748548541515')
                raise UserError((
                    "second Else"))
        else:
                raise UserError((
                    "Period Is Incorrect Or Age Is Incorrect "))


    @api.model
    def get_individual(self,data):
        if data.get('z') and data.get('d') and data.get('p_from') and data.get('p_to'):
            result = {}


            geographical_coverage=data.get('z')
            DOB=data.get('d')
            coverage_from=data.get('p_from')
            coverage_to=data.get('p_to')

            # dob=[DOB]
            days=self.calculate_period(coverage_from,coverage_to)
            age=self.calculate_age(DOB)

            data = self.env['quotation.price.setup'].search(
                [('zone', '=', geographical_coverage),('from_age','<=',age[0]),('to_age','>=',age[0])])

            opj = []
            for rec in data.price_lines:
                if days <= rec.period:
                    opj.append(rec.period)
            if opj:
                    min_period = min(opj)
                    print(min_period)
                    for record in data:
                        for rec in record.price_lines:
                          if rec.period == min_period:
                                    result['net'] = rec.net_premium*(record.currency_id.rate)
                                    result['pro_stamp'] = rec.proportional_stamp *(record.currency_id.rate)
                                    result['dimensional_stamp'] = rec.dimensional_stamp *(record.currency_id.rate)
                                    result['supervisory_stamp'] = rec.supervisory_stamp *(record.currency_id.rate)
                                    # self.issue_fees = record.issue_fees
                                    fra,result['gross'] = math.modf(rec.gross_premium *(record.currency_id.rate))
                                    result['issue_fees'] = (rec.issue_fees *(record.currency_id.rate))+(1-fra)

                                    print("fraction")
                                    print (fra)

            return result

    @api.model
    def calculate_age(self, DOB):
        ages = []
        for rec in DOB:
            today = datetime.today().date()
            if isinstance(rec, str) == True:
                DOB = datetime.strptime(rec, '%Y-%m-%d').date()
                difference = relativedelta(today, DOB)
            else:
                difference = relativedelta(today, rec)
            age = difference.years
            months = difference.months
            days = difference.days
            if months or days != 0:
                age += 1
            ages.append(age)
        return ages

    @api.model
    def calculate_period(self,when,to):
        if isinstance(when, str) == True:
            when = datetime.strptime(when, '%Y-%m-%d').date()
        if isinstance(to, str) == True:
            to = datetime.strptime(to, '%Y-%m-%d').date()
        period = (to - when).days
        return period

    


    