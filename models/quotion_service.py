from datetime import timedelta, datetime
import base64
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo import api, fields, models,exceptions
import  math

class QuotationService(models.Model):
    _name = 'quotation.service'

    lob = fields.Many2one('insurance.line.business', 'LOB', required=True, default=3)
    travel_package = fields.Selection([('individual', 'Individual'), ('family', 'Family')], 'Package For', default='individual')
    medical_package = fields.Selection([('individual', 'Individual'),
                                ('family', 'Family'),
                                ('sme', 'SME'), ],
                               'Package For')
    geographical_coverage = fields.Selection([('zone 1', 'Europe'),
                                              ('zone 2', 'Worldwide excluding USA & CANADA'),
                                              ('zone 3', 'Worldwide'), ],
                                             'Zone',
                                             default='zone 1')
    age = fields.Integer('Age', compute='compute_age', store=True)
    coverage_from = fields.Date('From', default=datetime.today(), required=True)
    coverage_to = fields.Date('To')
    days = fields.Integer('Day(s)', compute='compute_days', store='True', required=True)
    # motor_product = fields.Many2one('product.covers', 'Product')
    brand = fields.Selection([('all brands', 'All Brands (except Chinese & East Asia)'),
                              ('chinese cars & east asia', 'Chinese Cars & East Asia'), ('all models', 'All Models')],
                             'Brand')
    deductible = fields.Selection([('250 EGP', '250 EGP'),
                                   ('4 Per Thousand', '4 Per Thousand')],
                                  'Deductible')
    medical_product = fields.Many2one('medical.price', 'Product')
    motor_product = fields.Many2one('product.covers', 'Product')
    price = fields.Float('Premium')
    dob = fields.Date('Date OF Birth', default=datetime.today())
    sum_insured = fields.Float('Sum Insured')
    members = fields.One2many('members', 'quotation_id', string="Members")

    @api.depends('coverage_from', 'coverage_to')
    def compute_days(self):
        if self.coverage_from and self.coverage_to:
            # date1 = datetime.strptime(self.coverage_from, '%Y-%m-%d').date()
            # date2 = datetime.strptime(self.coverage_to, '%Y-%m-%d').date()
            date3 = (self.coverage_to - self.coverage_from).days
            self.days = date3

    @api.depends('dob')
    def compute_age(self):
        if self.dob:
            # date1 = datetime.strptime(str(self.issue_date), '%Y-%m-%d %H:%M:%S').date()
            # date2 = datetime.strptime(str(self.DOB), '%Y-%m-%d' ).date()
            difference = relativedelta(self.issue_date, self.DOB)
            age = difference.years
            months = difference.months
            days = difference.days
            if months or days != 0:
                age += 1
            self.age = age

    def calculate_age(self, DOB):
        ages = []
        for rec in DOB:
            today = datetime.today().date()
            DOB = rec
            difference = relativedelta(today, DOB)
            age = difference.years
            months = difference.months
            days = difference.days
            if months or days != 0:
                age += 1
            ages.append(age)
        return ages

    @api.onchange('medical_package')
    def product_domain(self):
        if self.medical_package == 'family':
            return {'domain': {'medical_product': [('package', '=', 'individual')]}}
        else:
            return {'domain': {'medical_product': [('package', '=', self.medical_package)]}}

    @api.onchange('brand', 'deductible', 'sum_insured','motor_product')
    def calculate_motor_price(self):

        if self.brand == 'all models':
            if self.sum_insured and self.motor_product:
                rate = self.env['motor.rating.table'].search(
                    [('brand', '=', 'all models'),
                     ('sum_insured_from', '<=', self.sum_insured), ('sum_insure_to', '>=', self.sum_insured),
                     ('product_id', '=', self.motor_product)])
                self.price = self.sum_insured * rate.rate
        else:

            if self.brand == 'all brands':
                if self.sum_insured and self.motor_product and self.deductible:
                    rate = self.env['motor.rating.table'].search([('brand', '=', self.brand),
                                                                  ('deductible', '=', self.deductible),
                                                                  ('sum_insured_from', '<=', self.sum_insured),
                                                                  ('sum_insure_to', '>=', self.sum_insured),
                                                                  ('product_id', '=', self.motor_product)])
                    self.price = self.sum_insured * rate.rate
            else:
                if self.sum_insured and self.motor_product:
                    rate = self.env['motor.rating.table'].search(
                        [('brand', '=', self.brand),
                         ('sum_insured_from', '<=', self.sum_insured),
                         ('sum_insure_to', '>=', self.sum_insured),
                         ('product_id', '=', self.motor_product)])
                    self.price = self.sum_insured * rate.rate

    def calculate_age(self, DOB):
        ages = []
        for rec in DOB:
            today = datetime.today().date()
            DOB = rec
            difference = relativedelta(today, DOB)
            age = difference.years
            months = difference.months
            days = difference.days
            if months or days != 0:
                age += 1
            ages.append(age)
        return ages


    # # @api.onchange('dob')
    # # @api.onchange('product')
    def get_family_ages(self):
        DOB = []
        for rec in self.members:
            DOB.append(rec.dob)
        return DOB

    @api.onchange('dob','members','medical_product')
    def calculate_price(self):
        if self.lob.line_of_business == 'Medical':
            if self.medical_package == 'individual':
                if self.medical_product:
                    dprice = {}
                    price = 0
                    ages = []
                    ages.append(self.dob)
                    # if data.get('type') == 'individual':
                    age = self.calculate_age(ages)
                    for record in self.env['medical.price'].search([('package', '=', 'individual'),
                                                                    ('product_name', '=', self.medical_product.product_name)]):
                        for rec in record.price_lines:
                            if rec.from_age <= age[0] and rec.to_age >= age[0]:
                                price = rec.price
                    self.write({"price": price})
            elif self.medical_package == 'family':
                if self.medical_product:
                    for record in self.env['medical.price'].search([('package', '=', 'individual'),
                                                                    ('product_name', '=', self.medical_product.product_name)]):
                        price = 0.0
                        for age in self.calculate_age(self.get_family_ages()):
                            for rec in record.price_lines:
                                if rec.from_age <= age and rec.to_age >= age:
                                    price += rec.price
                    self.write({"price": price})
            else:
                if self.medical_product:
                    for record in self.env['medical.price'].search([('package', '=', 'sme'),
                                                                    ('product_name', '=', self.medical_product.product_name)]):
                        price = 0.0
                        for age in self.calculate_age(self.get_family_ages()):
                            for rec in record.price_lines:
                                if rec.from_age <= age and rec.to_age >= age:
                                    price += rec.price
                    self.write({"price": price})
    #
    # def calculate_travel_price(self):
    #     if self.age and self.geographical_coverage and self.days:
    #         if self.travel_package == "individual":
    #             result = {}
    #             kid_dob = []
    #             if self.days > 0:
    #
    #         elif self.travel_package == "family":


    def motor(self):
        self.write({"lob": 3})

    def medical(self):
        self.write({"lob": 1})

class Members(models.Model):
    _name = 'members'

    dob = fields.Date('Date OF Birth')
    age = fields.Float('age')
    type = fields.Selection([('spouse', 'Spouse'),
                             ('kid', 'kid'),
                             ('brother', 'brother'),
                             ('sister', 'sister'),
                             ('parent', 'parent'),
                             ('grandparents', 'grandparents'),
                             ], default='spouse', string='Relationship')
    quotation_id = fields.Many2one('quotation.service')

    @api.model
    @api.onchange('dob')
    def get_age(self):
        if self.dob:

            today = datetime.today().date()
            difference = relativedelta(today, self.dob)
            age = difference.years
            months = difference.months
            days = difference.days
            if months or days != 0:
                age += 1
            self.age = age





