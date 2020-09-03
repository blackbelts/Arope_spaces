from odoo import api, fields, models
from odoo.exceptions import UserError
from datetime import timedelta, datetime
from odoo.http import request
from datetime import datetime
# from base64 import b64decode
import codecs
import requests



import logging
import werkzeug


from dateutil.relativedelta import relativedelta

import base64, os

time = [('12:00 AM', '12:00 AM'), ('12:30 AM', '12:30 AM'), ('01:00 AM', '01:00 AM'), ('01:30 AM', '01:30 AM'),
             ('02:00 AM', '02:00 AM'), ('02:30 AM', '02:30 AM'), ('03:00 AM', '03:00 AM'), ('03:30 AM', '03:30 AM'),
             ('04:00 AM', '04:00 AM'), ('04:30 AM', '04:30 AM'), ('05:00 AM', '05:00 AM'), ('05:30 AM', '05:30 AM'),
             ('06:00 AM', '06:00 AM'), ('06:30 AM', '06:30 AM'), ('07:00 AM', '07:00 AM'), ('07:30 AM', '07:30 AM'),
             ('08:00 AM', '08:00 AM'), ('08:30 AM', '08:30 AM'), ('09:00 AM', '09:00 AM'), ('09:30 AM', '09:30 AM'),
             ('10:00 AM', '10:00 AM'), ('10:30 AM', '10:30 AM'), ('11:00 AM', '11:00 AM'), ('11:30 AM', '11:30 AM'),
             ('12:00 PM', '12:00 PM'), ('12:30 PM', '12:30 PM'), ('01:00 PM', '01:00 PM'), ('01:30 PM', '01:30 PM'),
             ('02:00 PM', '02:00 PM'), ('02:30 PM', '02:30 PM'), ('03:00 PM', '03:00 PM'), ('03:30 PM', '03:30 PM'),
             ('04:00 PM', '04:00 PM'), ('04:30 PM', '04:30 PM'), ('05:00 PM', '05:00 PM'), ('05:30 PM', '05:30 PM'),
             ('06:00 PM', '06:00 PM'), ('06:30 PM', '06:30 PM'), ('07:00 PM', '07:00 PM'), ('07:30 PM', '07:30 PM'),
             ('08:00 PM', '08:00 PM'), ('08:30 PM', '08:30 PM'), ('09:00 PM', '09:00 PM'), ('09:30 PM', '09:30 PM'),
             ('10:00 PM', '10:00 PM'), ('10:30 PM', '10:30 PM'), ('11:00 PM', '11:00 PM'), ('11:30 PM', '11:30 PM')]

class Quotation(models.Model):
    _name = 'insurance.quotation'
    _rec_name = 'application_number'
    # insurance_type = fields.Selection([
    #     ('medical', 'Medical'),
    #     ('non-medical', 'Non-Medical')], string='Insurance Type', default='medical', )
    lob = fields.Many2one('insurance.line.business', 'LOB', required=True)
    product_id = fields.Many2one('insurance.product', 'Product', domain="[('line_of_bus', '=', lob)]")
    test_state = fields.Many2one('state.setup', domain="[('product_ids', 'in', product_id)]")
    # domain = "[('id', '!=', 26)]"
    name = fields.Char('Name', required=True)
    # contact = fields.Char('Contact', required=True)
    phone = fields.Char('Mobile', required=True)
    email = fields.Char('Email', required=True)
    target_price = fields.Float('Target Premium')
    application_number = fields.Char(string='Application Number', copy=False, index=True)
    application_date = fields.Date('Application Date', default=datetime.today(), readonly=True)
    quote_trials = fields.Char(string='Quote Trials')
    # questions_ids = fields.One2many('questionnaire.line.setup', 'application_id')
    # survey_ids = fields.One2many('survey.report', 'application_id')
    main_phone = fields.Char('Mobile Number (Main)')
    spare_phone = fields.Char('Mobile Number (Spare)')
    state = fields.Selection([
        ('quick_quote', 'Quote'),
        ('proposal', 'Fill Form'),
        ('survey_required', 'Survey Required'),
        ('surveyor', 'Assign Surveyor'),
        ('survey', 'Survey Report'),
        ('reinsurance', 'Reinsurance'),
        ('offer', 'Offer'),
        ('application', 'Upload Documents'),
        ('policy', 'Policy'),
        ('cancel', 'Rejected')], string='State')
    rejection_reason = fields.Selection([('price', 'Price'), ('benefits', 'Benefit')], sting="Reason")
    comment = fields.Text('Comment')
    recomm = fields.Text('Recommendation')
    sub_state = fields.Selection([('pending', 'Pending'), ('complete', 'Complete'), ('update', 'Update')], string="Sub State", readonly=True)


    address = fields.Char('Full Address')
    bussines_activity = fields.Char('Client business activity')
    sum_insured = fields.Float('Sum Insured')

    name_of_contact_person = fields.Char('Name OF Contact Person')
    # inspection_address = fields.Char('Full Inspection Address')
    # available_time_from = fields.Datetime('Available Time From')
    # available_time_to = fields.Datetime('To')
    # image = fields.Binary("Image", help="Select image here")
    questionnaire = fields.Binary("Upload Application")
    file_name = fields.Char("File Name")
    edit_questionnaire = fields.Binary("Questionnaire Edited")
    price = fields.Float('Premium')
    # member_ids = fields.One2many('members', 'quotation_id', 'Members')
    dob = fields.Date('Date OF Birth', default=datetime.today())
    product = fields.Many2one('medical.price', 'Product', domain="[('package', '=', package)]"
                              )
    application = fields.Binary("Application")
    final_price = fields.Float('Final Premium')
    # final_price = fields.Float('Final Price')
    final_application_ids = fields.One2many('final.application', 'application_id')
    # questions_ids = fields.One2many('insurances.answers', 'text_application_id')
    text_questions_ids = fields.One2many('insurances.answers', 'text_application_id')
    choose_questions_ids = fields.One2many('insurances.answers', 'choose_application_id')
    numerical_questions_ids = fields.One2many('insurances.answers', 'numerical_application_id')
    survey_report_ids = fields.One2many('survey.report', 'application_id')
    available_time_ids = fields.One2many('available.time', 'application_id', sting='Available Time')
    state_history_ids = fields.One2many('state.history', 'application_id')
    offer_ids = fields.One2many('final.offer', 'application_id')
    surveyor = fields.Many2one('res.users', 'Surveyor')
    policy_number = fields.Char('Policy Num')
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
    survey_date = fields.Datetime('Appointment')
    sub_answer_questionnaire = fields.Many2one('sub.questionnaire.answers', 'Sub Questionnaire')






    @api.onchange('state')
    def compute_state(self):
        self.test_state = self.env['state.setup'].search([('status', '=', self.state)]).id

    def create_pdf(self):
        return {
            'type': 'ir.actions.act_url',
            'url': 'http://207.154.195.214/questionnaire.docx',
            'target': 'self',
        }
    @api.onchange('brand','deductible','sum_insured')
    def calculate_motor_price(self):

        if self.brand == 'all models':
              rate = self.env['motor.rating.table'].search(
                    [('brand', '=', 'all models'),
                     ('sum_insured_from', '<=', self.sum_insured), ('sum_insure_to', '>=', self.sum_insured)])
              self.price = self.sum_insured*rate.rate
        else:

             if self.brand == 'all brands':
                    rate = self.env['motor.rating.table'].search([('brand','=', self.brand),
                                                                   ('deductible', '=', self.deductible),
                                                      ('sum_insured_from','<=', self.sum_insured),
                                                                   ('sum_insure_to', '>=', self.sum_insured)])
                    self.price = self.sum_insured * rate.rate
             else:
                   rate = self.env['motor.rating.table'].search(
                         [('brand', '=', self.brand),
                          ('sum_insured_from', '<=', self.sum_insured),
                          ('sum_insure_to', '>=', self.sum_insured)])
                   self.price = self.sum_insured * rate.rate



    @api.onchange('final_application_ids')
    def policy_pending(self):
        res = []
        if self.final_application_ids:
            for rec in self.final_application_ids:
                res.append(rec.application_files)
            if all(res):
                self.write({'state': 'policy'})
                self.env['state.history'].create({"application_id": self.id, "state": 'policy',
                                                  "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                                  "user": self.write_uid.id})
                self.test_state = self.env['state.setup'].search([('status', '=', 'policy')]).id
                self.write({'sub_state': 'pending'})

    def complete_and_proceed(self):
        self.write({'sub_state': 'complete'})
        if self.state == 'application':

            return {
                'type': 'ir.actions.act_window',
                'res_model': 'wizard.insurance.quotation',
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                               'default_insurance_app_id': self.id
                           }
            }
        elif self.state == 'surveyor':
            self.write({'state': 'survey'})
            self.env['state.history'].create({"application_id": self.id, "state": 'survey',
                                              "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                              "user": self.write_uid.id})
            self.test_state = self.env['state.setup'].search([('status', '=', 'survey')]).id
            self.write({'sub_state': 'pending'})

    @api.onchange('lob')
    def compute_application_number(self):
        if self.lob:
            number = self.env['ir.sequence'].next_by_code('application_number')
            currentYear = datetime.today().strftime("%Y")
            currentMonth = datetime.today().strftime("%m")
            self.write({'application_number' : self.lob.line_of_business.upper() + '/' + currentYear[2:4] + '/' + currentMonth +
                                               '/' + number})





    @api.onchange('product_id')
    def get_questions(self):
        if self.lob.line_of_business == 'Medical':
            # print('Medical')
            self.write({'state': 'quick_quote'})
            self.write({"test_state": self.env['state.setup'].search([('status', '=', 'quick_quote')]).id})

        elif self.lob.line_of_business == 'Motor':
            self.write({'state': 'quick_quote'})
            self.write({"test_state": self.env['state.setup'].search([('status', '=', 'quick_quote')]).id})
        else:
            self.write({'state': 'proposal'})
            self.write({"test_state": self.env['state.setup'].search([('status', '=', 'proposal')]).id})
            self.write({'sub_state': 'pending'})
        if self.text_questions_ids:
            for question in self.text_questions_ids:
                question.unlink()
        if self.choose_questions_ids:
            for question in self.choose_questions_ids:
                question.unlink()

        if self.numerical_questions_ids:
            for question in self.numerical_questions_ids:
                question.unlink()
        if self.survey_report_ids:
            for question in self.survey_report_ids:
                question.unlink()
        if self.final_application_ids:
            for question in self.final_application_ids:
                question.unlink()
        if self.offer_ids:
            for question in self.offer_ids:
                question.unlink()
        if self.product_id:
            # print(self.product_id)
            # self.questionnaire = self.product_id.questionnaire_file
            # self.file_name = self.product_id.file_name
            related_questions = self.env["questionnaire.line.setup"].search([("product_id.id", "=", self.product_id.id)])
            if related_questions:
                for question in related_questions:
                    if question.question_type == 'choose':
                        self.choose_questions_ids.create(
                            {"question": question.id, "choose_application_id": self.id})

                    elif question.question_type == 'numerical':
                        self.numerical_questions_ids.create(
                            {"question": question.id, "numerical_application_id": self.id})
                    else:
                        self.text_questions_ids.create(
                            {"question": question.id, "text_application_id": self.id})
            related_survey_questions = self.env["survey.line.setup"].search([("product_id.id", "=", self.product_id.id)])

            if related_survey_questions:
                for question in related_survey_questions:
                    self.env['survey.report'].create({"question": question.id, "desc": question.desc, "application_id": self.id})
            related_documents = self.env["final.application.setup"].search(
                [("product_id.id", "=", self.product_id.id)])
            if related_documents:
                for question in related_documents:
                    self.env['final.application'].create(
                        {"description": question.id, "application_id": self.id})
            related_offer_items = self.env["offer.setup"].search(
                [("product_id.id", "=", self.product_id.id)])
            if related_offer_items:
                for question in related_offer_items:
                    self.offer_ids.create(
                        {"question": question.id, "application_id": self.id})


    @api.onchange('dob','product')
    def compute_trial_number(self):
        if self.lob:
            number = self.env['ir.sequence'].next_by_code('trial_number')
            currentYear = datetime.today().strftime("%Y")
            self.write({"quote_trials" : self.lob.line_of_business.upper() + '/' + currentYear[2:4] + '/' + number})


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


    def approve_medical_price(self):
        self.write({'state': 'proposal'})
        self.env['state.history'].create({"application_id": self.id, "state": 'proposal',
                                          "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                          "user": self.write_uid.id})
        self.test_state = self.env['state.setup'].search([('status', '=', 'proposal')]).id
        self.write({'sub_state': 'pending'})

    def survey_confirm(self):
        self.write({'state': 'offer'})
        self.env['state.history'].create({"application_id": self.id, "state": 'offer',
                                          "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                          "user": self.write_uid.id})
        self.test_state = self.env['state.setup'].search([('status', '=', 'offer')]).id
        self.write({'sub_state': 'pending'})

    def survey_required(self):
        self.write({'state': 'survey_required'})
        self.env['state.history'].create({"application_id": self.id, "state": 'survey_required',
                                          "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                          "user": self.write_uid.id})
        self.test_state = self.env['state.setup'].search([('status', '=', 'survey_required')]).id
        self.write({'sub_state': 'pending'})

    def reinsurance_confirm(self):
            self.write({'state': 'reinsurance'})
            self.env['state.history'].create({"application_id": self.id, "state": 'reinsurance',
                                              "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                              "user": self.write_uid.id})
            self.test_state = self.env['state.setup'].search([('status', '=', 'reinsurance')]).id
            self.write({'sub_state': 'pending'})

    def assign_surveyor(self):
        self.write({'state': 'surveyor'})
        self.env['state.history'].create({"application_id": self.id, "state": 'surveyor',
                                          "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                          "user": self.write_uid.id})
        self.test_state = self.env['state.setup'].search([('status', '=', 'surveyor')]).id
        self.write({'sub_state': 'pending'})

    def submit_questionnaire(self):

        self.write({'state': 'submitted'})
        self.env['state.history'].create({"application_id": self.id, "state": 'submitted',
                                          "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                          "user": self.write_uid.id})

    def submit_survey_required(self):
        self.write({'state': 'survey'})
        self.env['state.history'].create({"application_id": self.id, "state": 'survey',
                                          "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                          "user": self.write_uid.id})
        self.test_state = self.env['state.setup'].search([('status', '=', 'survey')]).id
        self.write({'sub_state': 'pending'})

    def submit_survey(self):
        self.write({'state': 'survey_complete'})
        self.env['state.history'].create({"application_id": self.id, "state": 'survey_complete',
                                          "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                          "user": self.write_uid.id})
        self.test_state = self.env['state.setup'].search([('status', '=', 'survey_complete')]).id


    def final_confirm(self):
        self.write({'state': 'offer_ready'})
        self.env['state.history'].create({"application_id": self.id, "state": 'offer_ready',
                                          "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                          "user": self.write_uid.id})
        self.test_state = self.env['state.setup'].search([('status', '=', 'offer_ready')]).id



    def accept_offer(self):
        self.write({'state': 'application'})
        self.env['state.history'].create({"application_id": self.id, "state": 'application',
                                          "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                          "user": self.write_uid.id})
        self.test_state = self.env['state.setup'].search([('status', '=', 'application')]).id
        self.write({'sub_state': 'pending'})

    def issued(self):

        self.write({'state': 'policy'})

        self.test_state = self.env['state.setup'].search([('status', '=', 'policy')]).id
        self.write({"sub_state":'complete'})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'wizard.insurance.quotation',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_insurance_app_id':  self.id
            }

        }




    def reject(self):
        self.write({'state': 'cancel'})
        self.env['state.history'].create({"application_id": self.id, "state": 'cancel',
                                          "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                          "user": self.write_uid.id})
        self.test_state = self.env['state.setup'].search([('status', '=', 'cancel')]).id




class Members(models.Model):
    _name = 'members'

    name = fields.Char('Name')
    dob = fields.Date('Date OF Birth')
    relationship = fields.Char('Relationship')
    quotation_id = fields.Many2one('insurance.quotation')


class MedicalPriceTable(models.Model):
    _name = 'medical.price'
    _description = 'Set up Price tables'
    _rec_name = 'product_name'
    package = fields.Selection([('individual', 'Individual'),
                                ('family', 'Family'),
                                ('sme', 'SME'), ],
                               'Package For',
                               default='individual')

    product_name = fields.Char(string='Product Name')

    price_lines = fields.One2many('medical.price.line', 'price_id', string='Prices')



class MedicalPriceTableLines(models.Model):
    _name = 'medical.price.line'

    from_age = fields.Float('From Age')
    to_age = fields.Float('To Age')
    price = fields.Float('Price')
    price_id = fields.Many2one('medical.price', ondelete='cascade')

class Answers(models.Model):
    _name = 'insurances.answers'

    question = fields.Many2one('questionnaire.line.setup','Question')
    question_type = fields.Selection([('text', 'Text'), ('numerical', 'Numerical'), ('choose', 'Choose')],
                                     'Question Type', default='text')
    desc = fields.Char('Description')
    text = fields.Text('Answer')
    file = fields.Binary('File')
    value = fields.Float('Value')
    boolean = fields.Boolean('True Or False Answer', default=False)
    text_application_id = fields.Many2one('insurance.quotation', ondelete='cascade')
    choose_application_id = fields.Many2one('insurance.quotation', ondelete='cascade')
    numerical_application_id = fields.Many2one('insurance.quotation', ondelete='cascade')
    options = fields.Many2one('selection.options', 'Choose',ondelete='cascade')
    sub_answer_id = fields.Many2one('sub.questionnaire.answers', 'Sub Questionnaire', ondelete='cascade')





    @api.onchange('options')
    def set_member(self):
        if self.options.display_name == 'نعم' and self.question.sub_questionnaire_id != False:
            self.sub_answer_id = self.env['sub.questionnaire.answers'].create({'main_question' : self.question.id}).id
            print(self.sub_answer_id)
            for rec in self.question.sub_questionnaire_id.questionnaire_ids:
                # if self.sub_answer_id.answers == False:
                    self.env['insurances.answers'].create({"question": rec.id, "sub_answer_id": self.sub_answer_id.id})
                    print('15151515151516')

        ids = []
        for rec in self.question.options:
            ids.append(rec.id)

        return {'domain': {'options': [('id', 'in', ids)]}}


class SubQuestionnaireAnswers(models.Model):
    _name = 'sub.questionnaire.answers'
    _rec_name = 'main_question'

    main_question = fields.Many2one('questionnaire.line.setup', 'Main Question')
    answers = fields.One2many('insurances.answers', 'sub_answer_id')

class SurveyReport(models.Model):
    _name = 'survey.report'

    question = fields.Many2one('survey.line.setup','Survey Area')
    options = fields.Many2one('selection.options', 'Choose', ondelete='cascade', domain="[('survey_id', '=', question)]")
    desc = fields.Char('Description')
    text = fields.Text('Answer')
    file = fields.Binary('File')
    value = fields.Float('Value')
    boolean = fields.Boolean('True Or False Answer', default=False)
    application_id = fields.Many2one('insurance.quotation', ondelete='cascade')

class FinalOffer(models.Model):
    _name = 'final.offer'

    question = fields.Many2one('offer.setup','Offer Item')
    text = fields.Text('Value')
    file = fields.Binary('File')
    value = fields.Float('Value')
    application_id = fields.Many2one('insurance.quotation', ondelete='cascade')


class FinalApplication(models.Model):
    _name = 'final.application'

    description = fields.Many2one('final.application.setup', 'Document Name')
    application_files = fields.Binary('File')
    application_id = fields.Many2one('insurance.quotation', ondelete='cascade')

class AvailableTime(models.Model):
    _name = 'available.time'

    date = fields.Date('From Date')
    date_to = fields.Date('To Date')
    time_from = fields.Selection(time, "From", required=True)
    time_to = fields.Selection(time, "To", required=True)
    application_id = fields.Many2one('insurance.quotation', ondelete='cascade')

class stateHistory(models.Model):
    _name = 'state.history'

    state = fields.Selection([
        ('quick_quote', 'Quote'),
        ('proposal', 'Fill Form'),
        ('survey_required', 'Survey Required'),
        ('surveyor', 'Assign Surveyor'),
        ('survey', 'Survey Report'),
        ('reinsurance', 'Reinsurance'),
        ('offer', 'Offer'),
        ('application', 'Upload Documents'),
        ('policy', 'Policy'),
        ('cancel', 'Rejected')], string='State')

    datetime = fields.Datetime('Date')
    user = fields.Many2one('res.users', ondelete='cascade')
    application_id = fields.Many2one('insurance.quotation', ondelete='cascade')




class SelectionOptions(models.Model):
    _name = 'selection.options'
    _rec_name = 'option'
    option = fields.Char('Option')


class WizardInsuranceQuotation(models.TransientModel):
    _name = 'wizard.insurance.quotation'
    insurance_app_id = fields.Many2one('insurance.quotation')
    policy_number = fields.Char('Policy Num')

    def policy_num(self):
        self.insurance_app_id.write({'policy_number' : self.policy_number})


class FamilyAge(models.Model):
    _name = 'medical.family'

    name=fields.Char('name',required=True)
    type=fields.Selection([('spouse', 'Spouse'),
                           ('kid', 'kid'),
                           ('brother','brother'),
                           ('sister','sister'),
                           ('parent', 'parent'),
                           ('grandparents', 'grandparents'),
                           ],default='spouse')

    gender = fields.Selection([('M', 'Male'), ('F', 'Female')])
    age=fields.Float('age')
    DOB = fields.Date('Date Of Birth',required=True)
    application_id = fields.Many2one('insurance.quotation', ondelete='cascade')

    @api.model
    @api.onchange('DOB')
    def get_age(self):
        if self.DOB:

            today = datetime.today().date()
            difference = relativedelta(today, self.DOB)
            age = difference.years
            months = difference.months
            days = difference.days
            if months or days != 0:
                age += 1
            self.age = age


