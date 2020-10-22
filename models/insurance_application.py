from odoo import api, fields, models
from datetime import datetime




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
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _rec_name = 'application_number'
    # insurance_type = fields.Selection([
    #     ('medical', 'Medical'),
    #     ('non-medical', 'Non-Medical')], string='Insurance Type', default='medical', )
    lob = fields.Many2one('insurance.line.business', 'LOB', required=True)
    product_id = fields.Many2one('insurance.product', 'Product', domain="[('line_of_bus', '=', lob)]")
    test_state = fields.Many2one('state.setup', domain="[('product_ids', 'in', product_id),"
                                                       "('type', '=', 'insurance_app')]")
    # domain = "[('id', '!=', 26)]"
    name = fields.Char('Customer Name', required=True)
    # contact = fields.Char('Contact', required=True)
    phone = fields.Char('Customer Mobile', required=True)
    email = fields.Char('Customer Email', required=True)
    target_price = fields.Text('High Level Requirements')
    application_number = fields.Char(string='Application Number', copy=False, index=True)
    application_date = fields.Date('Application Date', default=datetime.today(), readonly=True)
    quote_trials = fields.Char(string='Quote Trials')
    # questions_ids = fields.One2many('questionnaire.line.setup', 'application_id')
    # survey_ids = fields.One2many('survey.report', 'application_id')
    main_phone = fields.Char('Mobile Number (Main)')
    spare_phone = fields.Char('Mobile Number (Spare)')
    state = fields.Selection([
        ('application_form', 'Application Form'),
        ('initial_offer', 'Initial Offer'),
        ('survey', 'Survey'),
        ('final_offer', 'Final Offer'),
        ('application', 'Issue In Progress'),
        ('policy', 'Policy Issued'),
        ('cancel', 'Lost')], string='State')
    rejection_reason = fields.Selection([('price', 'Price'), ('benefits', 'Benefit')], sting="Reason")
    comment = fields.Text('Comment')
    recomm = fields.Text('Recommendation')
    sub_state = fields.Selection([('pending', 'Pending'),('surveyor', 'Assign Surveyor'), ('complete', 'Submitted'),
                                  ('accepted', 'Accepted'),('cancel', 'Rejected')], string="Sub State", readonly=True)


    address = fields.Char('Full Address')
    bussines_activity = fields.Char('Client business activity')
    sum_insured = fields.Float('Sum Insured')

    name_of_contact_person = fields.Char('Survey Contact Person')
    # inspection_address = fields.Char('Full Inspection Address')
    # available_time_from = fields.Datetime('Available Time From')
    # available_time_to = fields.Datetime('To')
    # image = fields.Binary("Image", help="Select image here")
    questionnaire = fields.Many2many('ir.attachment', string="Download Application Form",relation="insurance_quotation_questionnaire")
    file_name = fields.Char("File Name")
    upload_questionnaire = fields.Many2many('ir.attachment', string="Upload Scanned Form",relation="insurance_quotation_issued_questionnaire")
    price = fields.Float('Premium')
    # member_ids = fields.One2many('members', 'quotation_id', 'Members')
    dob = fields.Date('Date OF Birth', default=datetime.today())
    product = fields.Many2one('medical.price', 'Product', domain="[('package', '=', package)]"
                              )
    application = fields.Binary("Application")
    final_price = fields.Float('Final Premium')
    # final_price = fields.Float('Final Price')
    final_application_ids = fields.One2many('final.application', 'quotation_id')
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
    policy_issue_date = fields.Date('Policy Issue Date')
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
    quote_state = fields.Selection([('pending', 'Pending'), ('accepted', 'Accepted'), ('cancel', 'Rejected')], string='Quote State', default='pending')
    request_for_ofer_state = fields.Selection([('pending', 'Pending'), ('complete', 'Submitted'),('accepted', 'Accepted')],
                                              string='Application Offer State', default='pending')
    survey_state = fields.Selection([('pending', 'Pending'),('surveyor', 'Surveyor Assigned'),
                                     ('complete', 'Submitted'), ('accepted', 'Accepted')], string='Survey State', default='surveyor')
    quotation_id = fields.Many2one('quotation.service')
    message = fields.Text('Description')
    persons = fields.One2many('persons.lines', 'application_id')

    @api.onchange('test_state','product_id')
    def get_message(self):
        if self.test_state:
            print('hhhhhhhhh')
            self.message = self.test_state.message

    @api.onchange('offer_ids')
    def change_offer(self):
        if self.offer_ids:
            offers = []
            for rec in self.offer_ids:
                offers.append(rec)
            if  offers[-1].offer_state == 'submitted':
                if offers[-1].type == 'initial':
                    self.write({'state': 'initial_offer'})
                    self.env['state.history'].create({"application_id": self.id, "state": 'initial_offer',
                                                      "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                                      "user": self.write_uid.id})
                    self.test_state = self.env['state.setup'].search(
                        [('status', '=', 'initial_offer'), ('type', '=', 'insurance_app')]).id
                    # related_documents = self.env["final.application.setup"].search(
                    #     [("product_id.id", "=", self.product_id.id)])
                    # if related_documents:
                    #     for question in related_documents:
                    #         if question.state == 'initial_offer':
                    #             if question.file:
                    #
                    #                 id = self.env['final.application'].create(
                    #                     {"description": question.id,
                    #                      "quotation_id": self.id})
                    #                 print(id)
                    #                 print(id.quotation_id)
                    #             else:
                    #                 self.env['final.application'].create(
                    #                     {"description": question.id,
                    #                      "quotation_id": self.id})

            elif offers[-1].offer_state == 'accepted':
                # if offers[-1].type == 'initial':
                #     self.write({'state': 'application_form'})
                #     self.env['state.history'].create({"application_id": self.id, "state": 'application_form',
                #                                       "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                #                                       "user": self.write_uid.id})
                #     self.test_state = self.env['state.setup'].search(
                #         [('status', '=', 'application_form'), ('type', '=', 'insurance_app')]).id
                    # related_documents = self.env["final.application.setup"].search(
                    #     [("product_id.id", "=", self.product_id.id)])
                    # if related_documents:
                    #     for question in related_documents:
                    #         if question.state == 'application_form':
                    #             if question.file:
                    #
                    #                 id = self.env['final.application'].create(
                    #                     {"description": question.id, 'download_files': [question.file.id],
                    #                      "quotation_id": self.id})
                    #                 print(id)
                    #                 print(id.quotation_id)
                    #             else:
                    #                 self.env['final.application'].create(
                    #                     {"description": question.id,
                    #                      "quotation_id": self.id})
                if  offers[-1].type == 'final':
                    self.write({'state': 'application'})
                    self.env['state.history'].create({"application_id": self.id, "state": 'application',
                                                      "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                                      "user": self.write_uid.id})
                    self.test_state = self.env['state.setup'].search(
                        [('status', '=', 'application'), ('type', '=', 'insurance_app')]).id
                    # related_documents = self.env["final.application.setup"].search(
                    #     [("product_id.id", "=", self.product_id.id)])
                    # if related_documents:
                    #     for question in related_documents:
                    #         if question.state == 'application':
                    #             if question.file:
                    #
                    #                 id = self.env['final.application'].create(
                    #                     {"description": question.id, 'download_files': [question.file.id],
                    #                      "quotation_id": self.id})
                    #                 print(id)
                    #                 print(id.quotation_id)
                    #             else:
                    #                 self.env['final.application'].create(
                    #                     {"description": question.id,
                    #                      "quotation_id": self.id})

    @api.onchange('surveyor')
    def change_survey_state(self):
        if self.surveyor:
            self.write({"survey_state": 'pending'})

    @api.onchange('state')
    def compute_state(self):
        if self.state:
            self.test_state = self.env['state.setup'].search([('status', '=', self.state),('type', '=', 'insurance_app')]).id

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



    # @api.onchange('final_application_ids')
    # def policy_pending(self):
    #     if self.final_application_ids:
    #         res = []
    #         if self.final_application_ids:
    #             for rec in self.final_application_ids:
    #                 res.append(rec.application_files)
    #             if all(res):
    #                 # self.write({'state': 'policy'})
    #                 # self.env['state.history'].create({"application_id": self.id, "state": 'policy',
    #                 #                                   "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    #                 #                                   "user": self.write_uid.id})
    #                 # self.test_state = self.env['state.setup'].search([('status', '=', 'policy'),('type', '=', 'insurance_app')]).id
    #                 self.write({'sub_state': 'complete'})

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
            self.test_state = self.env['state.setup'].search([('status', '=', 'survey'),('type', '=', 'insurance_app')]).id
            self.write({'sub_state': 'pending'})

    @api.onchange('lob')
    def compute_application_number(self):
        if self.lob:
            number = self.env['ir.sequence'].next_by_code('application_number')
            currentYear = datetime.today().strftime("%Y")
            currentMonth = datetime.today().strftime("%m")
            self.write({'application_number' : self.lob.line_of_business.upper() + '/' + currentYear[2:4] + '/' + currentMonth +
                                               '/' + number})

    # # @api.multi
    # def send_mail_template(self):
    #     # Find the e-mail template
    #     template = self.env.ref('mail_template_demo.example_email_template')

    # First Function To Update


    @api.onchange('product_id')
    def get_questions(self):
        self.write({'state': 'application_form'})
        self.write({"test_state": self.env['state.setup'].search(
            [('status', '=', 'application_form'), ('type', '=', 'insurance_app')]).id})
        # if self.survey_report_ids:
        #     for question in self.survey_report_ids:
        #         question.unlink()
        #     if self.final_application_ids:
        #         for question in self.final_application_ids:
        #             question.unlink()
        # if self.product_id:
        # print(self.product_id)
        # self.questionnaire = self.product_id.questionnaire_file
        # self.file_name = self.product_id.file_name
        # related_questions = self.env["questionnaire.line.setup"].search([("product_id.id", "=", self.product_id.id)])
        # if related_questions:
        #     for question in related_questions:
        #         if question.question_type == 'choose':
        #             self.choose_questions_ids.create(
        #                 {"question": question.id, "choose_application_id": self.id})
        #
        #         elif question.question_type == 'numerical':
        #             self.numerical_questions_ids.create(
        #                 {"question": question.id, "numerical_application_id": self.id})
        #         else:
        #             self.text_questions_ids.create(
        #                 {"question": question.id, "text_application_id": self.id})

        # related_documents = self.env["final.application.setup"].search(
        #     [("product_id.id", "=", self.product_id.id)])
        # if related_documents:
        #     for question in related_documents:
        #         if question.state == 'proposal':
        #             if question.file:
        #
        #                 id= self.env['final.application'].create(
        #                     {"description": question.id,'download_files': [question.file.id],
        #                      "quotation_id": self.id})
        #                 print(id)
        #                 print(id.quotation_id)
        #             else:
        #                 self.env['final.application'].create(
        #                     {"description": question.id,
        #                      "quotation_id": self.id})
        # id.write({'download_file':
        #         [(0,0,{'name': 'Questionnaire', 'res_name': 'questionnaire',
        #                                                         'type': 'binary',
        #                                                         'datas': question.file[0].datas})],})
        # related_offer_items = self.env["offer.setup"].search(
        #     [("product_id.id", "=", self.product_id.id)])
        # if related_offer_items:
        #     for question in related_offer_items:
        #         self.offer_ids.create(
        #             {"question": question.id, "application_id": self.id})

    @api.onchange('persons')
    def get_application_form(self):
        all_persons = []
        for rec in self.persons:
            all_persons.append(rec)
            rec.write({'download_files': [self.product_id.questionnaire_file.id],
                       'insured': 'Insurer'+ str(len(all_persons))})


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

    @api.model
    def approve_price(self):
        self.write({'state': 'proposal'})
        self.env['state.history'].create({"application_id": self.id, "state": 'quick_quote','sub_state': 'accepted',
                                          "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                          "user": self.write_uid.id})
        self.env['state.history'].create({"application_id": self.id, "state": 'proposal','sub_state': 'pending',
                                          "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                          "user": self.write_uid.id})
        self.test_state = self.env['state.setup'].search([('status', '=', 'proposal'),
                                                          ('type', '=', 'insurance_app')]).id
        self.write({'quote_state': 'accepted'})
        self.write({'request_for_ofer_state': 'pending'})
        return True



    def survey_confirm(self):
        self.write({'state': 'offer'})
        self.env['state.history'].create({"application_id": self.id, "state": 'offer',
                                          "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                          "user": self.write_uid.id})
        self.test_state = self.env['state.setup'].search([('status', '=', 'offer'),('type', '=', 'insurance_app')]).id
        self.write({'sub_state': 'pending'})

    def initial_offer(self):
        self.write({'state': 'initial_offer'})
        self.env['state.history'].create({"application_id": self.id, "state": 'initial_offer',
                                          "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                          "user": self.write_uid.id})
        self.test_state = self.env['state.setup'].search([('status', '=', 'initial_offer'),('type', '=', 'insurance_app')]).id
        # related_documents = self.env["final.application.setup"].search(
        #     [("product_id.id", "=", self.product_id.id)])
        # if related_documents:
        #     for question in related_documents:
        #         if question.state == 'initial_offer':
        #             if question.file:
        #
        #                 id = self.env['final.application'].create(
        #                     {"description": question.id, 'download_files': [question.file.id],
        #                      "quotation_id": self.id})
        #                 print(id)
        #                 print(id.quotation_id)
        #             else:
        #                 self.env['final.application'].create(
        #                     {"description": question.id,
        #                      "quotation_id": self.id})
    def final_offer(self):
        self.write({'state': 'final_offer'})
        self.env['state.history'].create({"application_id": self.id, "state": 'final_offer',
                                          "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                          "user": self.write_uid.id})
        self.test_state = self.env['state.setup'].search(
            [('status', '=', 'final_offer'), ('type', '=', 'insurance_app')]).id
        self.message = self.test_state.message
        # related_documents = self.env["final.application.setup"].search(
        #     [("product_id.id", "=", self.product_id.id)])
        # if related_documents:
        #     for question in related_documents:
        #         if question.state == 'final_offer':
        #             if question.file:
        #
        #                 id = self.env['final.application'].create(
        #                     {"description": question.id, 'download_files': [question.file.id],
        #                      "quotation_id": self.id})
        #                 print(id)
        #                 print(id.quotation_id)
        #             else:
        #                 self.env['final.application'].create(
        #                     {"description": question.id,
        #                      "quotation_id": self.id})

    def survey(self):

        number = self.env['ir.sequence'].next_by_code('survies')
        currentYear = datetime.today().strftime("%Y")
        currentMonth = datetime.today().strftime("%m")

        self.env['survey.report'].create(
            {"name": "Survey"+ '/' + currentYear[2:4] + '/' + currentMonth + '/' + number,
             "type": 'insurance_application',
             "application_id": self.id,'state': 'pending', 'status': self.env['state.setup'].search([('survey_status', '=', 'pending'),('type', '=', 'survey')]).id,
             'message':self.env['state.setup'].search([('survey_status', '=', 'pending'),('type', '=', 'survey')]).message,
             "lob": self.lob.id, 'product_id': self.product_id.id,"customer_name": self.name, 'phone': self.phone, 'email': self.email,
             'application_date': self.application_date})

        self.write({"state":'survey'})
        self.env['state.history'].create({"application_id": self.id, "state": 'survey',
                                          "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                          "user": self.write_uid.id})
        self.test_state = self.env['state.setup'].search([('status', '=', 'survey'),('type', '=', 'insurance_app')]).id
        self.message = self.test_state.message


    def reinsurance_confirm(self):
            self.write({'state': 'reinsurance'})
            self.env['state.history'].create({"application_id": self.id, "state": 'reinsurance',
                                              "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                              "user": self.write_uid.id})
            self.test_state = self.env['state.setup'].search([('status', '=', 'reinsurance'),('type', '=', 'insurance_app')]).id
            self.write({'sub_state': 'pending'})

    def assign_surveyor(self):
        self.write({'sub_state': 'pending'})
        # self.env['state.history'].create({"application_id": self.id, "state": 'surveyor',
        #                                   "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        #                                   "user": self.write_uid.id})
        # self.test_state = self.env['state.setup'].search([('status', '=', 'surveyor'),('type', '=', 'insurance_app')]).id
        # self.write({'sub_state': 'pending'})

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
        self.test_state = self.env['state.setup'].search([('status', '=', 'survey'),('type', '=', 'insurance_app')]).id
        self.write({'sub_state': 'pending'})

    def submit_survey(self):
        self.write({'state': 'survey_complete'})
        self.env['state.history'].create({"application_id": self.id, "state": 'survey_complete',
                                          "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                          "user": self.write_uid.id})
        self.test_state = self.env['state.setup'].search([('status', '=', 'survey_complete'),('type', '=', 'insurance_app')]).id


    def final_confirm(self):
        self.write({'state': 'offer_ready'})
        self.env['state.history'].create({"application_id": self.id, "state": 'offer_ready',
                                          "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                          "user": self.write_uid.id})
        self.test_state = self.env['state.setup'].search([('status', '=', 'offer_ready'),('type', '=', 'insurance_app')]).id

    def get_history(self):
        # tree_view_id = self.env.ref("Arope-spaces.state_history_view_tree").id
        # ctx = dict(self.env.context)
        # ctx.update({
        #     'quotation_id': self.id,'name':'test', 'lob': self.lob
        # })
        self.ensure_one()
        return {
            'name': 'State History',
            'res_model': 'state.history',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'domain': [('application_id', '=', self.id)],
            'context': {
                "create": False,
            },
        }

    def get_survey(self):
        # tree_view_id = self.env.ref("Arope-spaces.state_history_view_tree").id
        # ctx = dict(self.env.context)
        # ctx.update({
        #     'quotation_id': self.id,'name':'test', 'lob': self.lob
        # })
        self.ensure_one()
        return {
            'name': 'Survey Report',
            'res_model': 'survey.report',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'domain': [('application_id', '=', self.id)],
            'context': {
                "create": False,
            },
        }



    def accept_offer(self):
        self.write({'state': 'application'})
        self.env['state.history'].create({"application_id": self.id, "state": 'application',
                                          "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                          "user": self.write_uid.id})
        self.test_state = self.env['state.setup'].search([('status', '=', 'application'),('type', '=', 'insurance_app')]).id
        self.write({'sub_state': 'pending'})

    def offer_accept(self):
        # self.write({'state': 'offer'})
        self.write({'sub_state': 'accepted'})
        # self.sub_state = 'accepted'

    def issued(self):

        self.write({'state': 'policy'})

        self.test_state = self.env['state.setup'].search([('status', '=', 'policy'),('type', '=', 'insurance_app')]).id
        self.message = self.test_state.message
        self.write({"sub_state":'complete'})
        self.env['state.history'].create({"application_id": self.id, "state": 'policy',
                                          "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                          "user": self.write_uid.id})
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

    def related_quote(self):
        self.ensure_one()
        return {
            'name': 'Related Quick Quote',
            'res_model': 'quotation.service',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'domain': [('id', '=', self.quotation_id.id)],
            'context': {
                "create": False,
            },
        }




    def reject(self):
        # if self.state == 'offer':
        #     self.write({'sub_state': 'cancel'})
        # else:
            self.write({'state': 'cancel'})
            self.env['state.history'].create({"application_id": self.id, "state": 'cancel',
                                              "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                              "user": self.write_uid.id})
            self.test_state = self.env['state.setup'].search([('status', '=', 'cancel'),('type', '=', 'insurance_app')]).id
            self.message = self.test_state.message


    def get_options_of_question(self):
        result = []
        options = []
        for rec in self.choose_questions_ids:
            for option in rec.question.options:
                options.append(option.option)

            result.append({'question': rec.question.question, 'options': options})
        return result





#
# class MedicalPriceTable(models.Model):
#     _name = 'medical.price'
#     _description = 'Set up Price tables'
#     _rec_name = 'product_name'
#     package = fields.Selection([('individual', 'Individual'),
#                                 ('family', 'Family'),
#                                 ('sme', 'SME'), ],
#                                'Package For',
#                                default='individual')
#
#     product_name = fields.Char(string='Product Name')
#
#     price_lines = fields.One2many('medical.price.line', 'price_id', string='Prices')

#
#
# class MedicalPriceTableLines(models.Model):
#     _name = 'medical.price.line'
#
#     from_age = fields.Float('From Age')
#     to_age = fields.Float('To Age')
#     price = fields.Float('Price')
#     price_id = fields.Many2one('medical.price', ondelete='cascade')

class Answers(models.Model):
    _name = 'insurances.answers'

    question = fields.Many2one('questionnaire.line.setup','Question')
    question_type = fields.Selection([('text', 'Text'), ('numerical', 'Numerical'), ('choose', 'Choose')],
                                     'Question Type', default='text')
    desc = fields.Char('Description')
    text = fields.Text('Answer')
    file = fields.Many2many('ir.attachment', string="Upload File")
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

class SurveyReportLine(models.Model):
    _name = 'survey.report.line'

    question = fields.Many2one('survey.line.setup','Survey Area')
    file = fields.Many2many('ir.attachment', string="Upload File")
    state = fields.Selection([('pending', 'Pending'), ('submitted', 'Submitted'),
                              ('accepted', 'Accepted'),('rejected', 'Rejected')], 'State')
    survey_id = fields.Many2one('survey.report', ondelete='cascade')

    @api.onchange('file')
    def change_state(self):
        if self.file != False:
            self.state = 'submitted'

class FinalOffer(models.Model):
    _name = 'final.offer'

    # question = fields.Many2one('offer.setup','Offer Item')
    type = fields.Selection([('initial', 'Initial Offer'), ('final', 'Final Offer')])
    date = fields.Date('Offer Date',default=lambda self:fields.datetime.today())
    comment = fields.Text('Comment')
    file = fields.Many2many('ir.attachment', string="Offer")
    value = fields.Float('Value')
    application_id = fields.Many2one('insurance.quotation', ondelete='cascade')
    offer_state = fields.Selection([('submitted', 'Submitted'),
                                    ('accepted', 'Accepted'), ('cancel', 'Rejected')], string='State')

    @api.onchange('file')
    def change_state(self):
        if self.file:
            self.offer_state = 'submitted'

class FinalApplication(models.Model):
    _name = 'final.application'

    description = fields.Many2one('final.application.setup', 'Document Name')
    download_files = fields.Many2many('ir.attachment', string="Download File")
    application_file = fields.Many2many('ir.attachment', string="Upload File", relation="final_application_uploads")
    issue_in_progress_state = fields.Selection(
        [('pending', 'Pending'), ('complete', 'Submitted'), ('accepted', 'Accepted'), ('cancel', 'Rejected')],
        string='State', default='pending')

    quotation_id = fields.Many2one('insurance.quotation', ondelete='cascade')

    @api.onchange('application_file')
    def change_state(self):
        if self.application_file:
            self.write({"issue_in_progress_state": 'complete'})



class FinalApplications(models.Model):
    _name = 'final.applications'

# class Final(models.Model):
#     _name = 'wizard.final.application'

class WizardFinalApplication(models.Model):
    _name = 'wizard.required.documents'

    insurance_app_id = fields.Many2one('insurance.quotation')
    insurer_id = fields.Many2one('persons.lines')
    required_documents = fields.Many2many('final.application')



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
        ('application_form', 'Application Form'),
        ('initial_offer', 'Initial Offer'),
        ('survey', 'Survey'),
        ('final_offer', 'Final Offer'),
        ('application', 'Issue In Progress'),
        ('policy', 'Policy Issued'),
        ('cancel', 'Lost')], string='State')
    sub_state = fields.Selection([('pending', 'Pending'),('surveyor', 'Assign Surveyor'), ('complete', 'Submitted'),
                                  ('accepted', 'Accepted'),('cancel', 'Rejected')], string="Sub State", readonly=True)

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
    policy_issue_date = fields.Date('Policy Issue Date', default=datetime.today())

    def policy_num(self):
        self.insurance_app_id.write({'policy_number' : self.policy_number, "policy_issue_date": self.policy_issue_date})

class SurveyReport(models.Model):

    _name = 'survey.report'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    type = fields.Selection([('insurance_application', 'Insurance Application'),
                             ('motor_claim', 'Motor Claim'),
                             ('non_motor_claim', 'Non Motor Claim')])
    survey_type = fields.Selection([('pre_survey', 'Pre Survey'),
                                    ('Survey_after_repair', 'Survey After Repair')])
    lob = fields.Many2one('insurance.line.business', 'LOB')
    product_id = fields.Many2one('insurance.product', 'Product', domain="[('line_of_bus', '=', lob)]")
    customer_name = fields.Char('Customer Name')
    phone = fields.Char('Customer Mobile')
    email = fields.Char('Customer Email')
    application_date = fields.Date('Application Date', default=datetime.today(), readonly=True)

    name = fields.Char("Survey Number", required=True, copy=False, index=True,
                             default=lambda self: self.env['ir.sequence'].next_by_code('survey'), readonly=True)

    state = fields.Selection([('pending', 'Pending'), ('surveyor', 'Surveyor Assigned'),
                            ('submitted', 'Submitted'), ('accepted', 'Accepted')], 'State', default='pending')
    status = fields.Many2one('state.setup', domain="[('type', '=', 'survey')]")
    surveyor = fields.Many2one('res.users', 'Surveyor')
    survey_report = fields.Many2many('ir.attachment', string='Upload Survey Report')
    comment = fields.Text('Comment')
    recomm = fields.Text('Recommendation')

    survey_report_ids = fields.One2many('survey.report.line', 'survey_id')

    application_id = fields.Many2one('insurance.quotation', ondelete='cascade', string='Application')
    claim_id = fields.Many2one('claim.app', ondelete='cascade', string='Application')
    message = fields.Text('Description')

    @api.onchange('status')
    def get_message(self):
        if self.status:
            self.message = self.status.message


    @api.onchange('survey_report')
    def survey_submitted(self):
        if self.survey_report:
            self.state = 'submitted'
            self.status = self.env['state.setup'].search([('survey_status', '=', 'submitted'),('type', '=', 'survey')]).id
            self.message = self.status.message

    def assign_surveyor(self):
        self.write({'state': 'surveyor'})
        self.status = self.env['state.setup'].search([('survey_status', '=', 'surveyor'), ('type', '=', 'survey')]).id
        self.application_id.write({'surveyor': self.surveyor.id})
        self.message = self.status.message

    def accept_survey(self):
        self.write({'state': 'accepted'})
        self.status = self.env['state.setup'].search([('survey_status', '=', 'accepted'), ('type', '=', 'survey')]).id
        self.message = self.status.message




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
            
class SurveyQuestions(models.Model):

    _inherit = 'survey.survey'
    product_id = fields.Many2one('insurance.product', 'Product')

    @api.onchange('product_id')
    def get_title(self):
        self.title = self.product_id.product_name




class PersonsLines(models.Model):

    _name = 'persons.lines'

    insured = fields.Char("Insured")
    comment = fields.Text('Comment')
    application_id = fields.Many2one('insurance.quotation', ondelete='cascade')
    download_files = fields.Many2many('ir.attachment', string="Download File")
    application_file = fields.Many2many('ir.attachment', string="Upload File",
                                        relation="wizard_required_documents_uploads")
    issue_in_progress_state = fields.Selection(
        [('pending', 'Pending'), ('complete', 'Submitted'), ('accepted', 'Accepted'), ('cancel', 'Rejected')],
        string='State', default='pending')

    @api.onchange('application_file')
    def change_state(self):
        if self.application_file:
            self.write({"issue_in_progress_state": 'complete'})


    # def start_application(self):
    #     self.ensure_one()
    #     # create a response and link it to this applicant
    #     user = self.env['res.users'].search([('id', '=', self._uid)])
    #     if not self.response_id:
    #         for rec in self.env['survey.survey'].search([('product_id', '=', self.application_id.product_id.id)]):
    #             response = rec._create_answer(user=user)
    #             self.response_id = response.id
    #     else:
    #         response = self.response_id
    #     for rec in self.env['survey.survey'].search([('product_id', '=', self.application_id.product_id.id)]):
    #     # grab the token of the response and start surveying
    #         return rec.with_context(survey_token=response.token).action_start_survey()

    def required_document(self):

        ids = []
        if not self.env['wizard.required.documents'].search([('insurer_id', '=', self.id)]):
            related_documents = self.env["final.application.setup"].search(
                [("product_id.id", "=", self.application_id.product_id.id)])
            if related_documents:
                for question in related_documents:
                    id = self.env['final.application'].create(
                        {"description": question.id,
                         "quotation_id": self.id})
                    ids.append(id.id)


            return {
                'type': 'ir.actions.act_window',
                'res_model': 'wizard.required.documents',
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'new',
                'domain': [('insurer_id', '=', self.id)],
                'context': {
                    'default_insurer_id':self.id,
                    'default_insurance_app_id': self.application_id.id,
                    'default_required_documents': ids


                }
            }
        else:
            self.ensure_one()
            return {
                'name': 'Related Quick Quote',
                'res_model': 'wizard.required.documents',
                'type': 'ir.actions.act_window',
                'view_mode': 'tree,form',
                'domain': [('insurer_id', '=', self.id)],
                'context': {
                    "create": False,
                },
            }








