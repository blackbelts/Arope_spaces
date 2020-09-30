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
    family_age = fields.One2many('medical.family', 'application_id', string='Members')
    package = fields.Selection([('individual', 'Individual'),
                                ('family', 'Family'),
                                ('sme', 'SME'), ],
                               'Package For',
                               default='individual')
    # motor_product = fields.Many2one('product.covers', 'Product')
    brand = fields.Selection([('all brands', 'All Brands (except Chinese & East Asia)'),
                              ('chinese cars & east asia', 'Chinese Cars & East Asia'), ('all models', 'All Models')],
                             'Brand')
    deductible = fields.Selection([('250 EGP', '250 EGP'),
                                   ('4 Per Thousand', '4 Per Thousand')],
                                  'Deductible')
    product = fields.Many2one('medical.price', 'Product', domain="[('package', '=', package)]"
                              )
    price = fields.Float('Premium')
    dob = fields.Date('Date OF Birth', default=datetime.today())
    sum_insured = fields.Float('Sum Insured')

    @api.onchange('brand', 'deductible', 'sum_insured')
    def calculate_motor_price(self):

        if self.brand == 'all models':
            rate = self.env['motor.rating.table'].search(
                [('brand', '=', 'all models'),
                 ('sum_insured_from', '<=', self.sum_insured), ('sum_insure_to', '>=', self.sum_insured)])
            self.price = self.sum_insured * rate.rate
        else:

            if self.brand == 'all brands':
                rate = self.env['motor.rating.table'].search([('brand', '=', self.brand),
                                                              ('deductible', '=', self.deductible),
                                                              ('sum_insured_from', '<=', self.sum_insured),
                                                              ('sum_insure_to', '>=', self.sum_insured)])
                self.price = self.sum_insured * rate.rate
            else:
                rate = self.env['motor.rating.table'].search(
                    [('brand', '=', self.brand),
                     ('sum_insured_from', '<=', self.sum_insured),
                     ('sum_insure_to', '>=', self.sum_insured)])
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

    # @api.onchange('dob')
    # @api.onchange('product')
    def get_family_ages(self):
        DOB = []
        for rec in self.family_age:
            DOB.append(rec.DOB)
        return DOB

    @api.onchange('dob','family_age','product')
    def calculate_price(self):
        if self.lob.line_of_business == 'Medical':
            if self.package == 'individual':
                if self.product:
                    dprice = {}
                    price = 0
                    ages = []
                    ages.append(self.dob)
                    # if data.get('type') == 'individual':
                    age = self.calculate_age(ages)
                    for record in self.env['medical.price'].search([('package', '=', 'individual'),
                                                                    ('product_name', '=', self.product.product_name)]):
                        for rec in record.price_lines:
                            if rec.from_age <= age[0] and rec.to_age >= age[0]:
                                price = rec.price
                    self.write({"price": price})
            elif self.package == 'family':
                if self.product:
                    for record in self.env['medical.price'].search([('package', '=', 'individual')]):
                        price = 0.0
                        for age in self.calculate_age(self.get_family_ages()):
                            for rec in record.price_lines:
                                if rec.from_age <= age and rec.to_age >= age:
                                    price += rec.price
                    self.write({"price": price})
            else:
                if self.product:
                    for record in self.env['medical.price'].search([('package', '=', 'sme')]):
                        price = 0.0
                        for age in self.calculate_age(self.get_family_ages()):
                            for rec in record.price_lines:
                                if rec.from_age <= age and rec.to_age >= age:
                                    price += rec.price
                    self.write({"price": price})


    def motor(self):
        self.write({"lob": 3})

    def medical(self):
        self.write({"lob": 1})

    # def travel(self):
    #     self.write({"lob": 3})


