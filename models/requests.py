from datetime import timedelta, datetime
import base64
from xlrd import open_workbook
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo import api, tools, fields, models


class CrmLeads(models.Model):
    _inherit = "crm.lead"
    opp_type = fields.Selection([('insurance_app', 'Insurance Application'),
                                ('motor_claim', 'Motor Claim'),('general_claim', 'General Claim'),
                                 ('end', 'Endorsement'),('renew', 'Renewal'),('cancel', 'Cancellation'),
                                 ('quote','Quote'),('signup','Sign Up')],string='Type')
    state = fields.Selection([
        ('application_form', 'Application Form'),
        ('initial_offer', 'Initial Offer'),
        ('survey', 'Survey'),
        ('final_offer', 'Final Offer'),
        ('application', 'Issue In Progress'),
        ('policy', 'Policy Issued'),
        ('cancel', 'Lost')], string='State')
    lob = fields.Many2one('insurance.line.business', 'LOB')
    product_id = fields.Many2one('insurance.product', 'Product', domain="[('line_of_bus', '=', lob)]")
    customer_name = fields.Char('Customer Name')
    phone = fields.Char('Customer Mobile')
    email = fields.Char('Customer Email')
    application_number = fields.Char(string='Application Number', copy=False, index=True)
    application_date = fields.Date('Application Date', default=datetime.today(), readonly=True)
    policy_number = fields.Char('Policy Num')
    policy_issue_date = fields.Date('Policy Issue Date')
    name_of_contact_person = fields.Char('Survey Contact Person')
    main_phone = fields.Char('Mobile Number (Main)')
    spare_phone = fields.Char('Mobile Number (Spare)')
    persons = fields.One2many('persons.lines', 'opp_id')
    offer_ids = fields.One2many('final.offer', 'opp_id')

    # @api.onchange('offer_ids')
    def change_offer(self):
        if self.offer_ids:
            offers = []
            for rec in self.offer_ids:
                offers.append(rec)
            if offers[-1].offer_state == 'submitted':
                if offers[-1].type == 'initial':
                    self.write({'state': 'initial_offer'})
                    self.env['state.history'].create({"application_id": self.id, "state": 'initial_offer',
                                                      "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                                      "user": self.write_uid.id})
                    self.test_state = self.env['state.setup'].search(
                        [('status', '=', 'initial_offer'), ('type', '=', 'insurance_app')]).id
                    self.message = self.test_state.message
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
                if offers[-1].type == 'final':
                    self.write({'state': 'application'})
                    self.env['state.history'].create({"application_id": self.id, "state": 'application',
                                                      "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                                      "user": self.write_uid.id})
                    self.test_state = self.env['state.setup'].search(
                        [('status', '=', 'application'), ('type', '=', 'insurance_app')]).id
                    self.message = self.test_state.message
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


    # @api.onchange('state')
    def compute_state(self):
        if self.state:
            self.test_state = self.env['state.setup'].search(
                [('status', '=', self.state), ('type', '=', 'insurance_app')]).id

    @api.onchange('lob')
    def compute_application_number(self):
        if self.lob:
            number = self.env['ir.sequence'].next_by_code('application_number')
            currentYear = datetime.today().strftime("%Y")
            currentMonth = datetime.today().strftime("%m")
            self.write(
                {'application_number': self.lob.line_of_business.upper() + '/' + currentYear[2:4] + '/' + currentMonth +
                                       '/' + number})


    # @api.onchange('product_id')
    def get_questions(self):
        self.write({'state': 'application_form'})
        self.write({"test_state": self.env['state.setup'].search(
            [('status', '=', 'application_form'), ('type', '=', 'insurance_app')]).id})


    @api.onchange('persons')
    def get_application_form(self):
        all_persons = []
        for rec in self.persons:
            all_persons.append(rec)
            rec.write({'download_files': [self.product_id.questionnaire_file.id],
                       'insured': 'Insurer'+ str(len(all_persons))})
