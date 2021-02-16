from datetime import timedelta, datetime
import base64
from xlrd import open_workbook
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo import api, tools, fields, models


class CrmLeads(models.Model):
    _inherit = "crm.lead"

    opp_type = fields.Many2one('request.type',string='Type')
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
    # stage_id = fields.Many2one('crm.stage', domain="['|',('type', '=', 'opp_type'),('type', '=', False)]")
    message = fields.Text('Description')

    @api.onchange('opp_type')
    @api.constrains('opp_type')
    def stage_domain(self):
        if self.stage_id:
            self.message = self.stage_id.message
        return {'domain': {'stage_id': ['|',('type', 'in', self.opp_type.id),('type', '=', False)]}}

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
    question_ids = fields.One2many('insurances.answers', 'request_id')
    name = fields.Char('Request')
    @api.model
    def create(self, vals):
        serial_no = self.env['ir.sequence'].next_by_code('req')
        # merge code and serial number
        vals['name'] = str(serial_no)

        return super(CrmLeads, self).create(vals)

    name = fields.Char('Request', required=False, readonly=True)
    policy = fields.Char(string='Policy')
    policy_seq = fields.Many2one('insurance.product', string='product')
    product = fields.Char('Policy Product')
    customer = fields.Char('Customer')
    start_date = fields.Date('Effective From')
    end_date = fields.Date('Effective To')
    quotation_id = fields.Many2one('quotation.service')
    # state = fields.Selection([('pending', 'Pending'),
    #                           ('submitted', 'Submitted'), ('issued', 'Issued')], 'State', default='pending')
    #claim
    claim_number = fields.Char(string='Claim Number', copy=False, index=True)
    lob = fields.Many2one('insurance.line.business', 'LOB')
    customer_name = fields.Char('Customer Name')
    phone = fields.Char('Customer Mobile')
    claim_product = fields.Many2one('insurance.product', 'Product')
    policy_num = fields.Char(string="Policy Number", copy=True)
    chasse_num = fields.Char(string="Chasse No", copy=True)
    maintenance_centers_in_or_out = fields.Selection([('in', 'Arope Network'), ('out', 'Outside Arope Network')],
                                                     string='Service Center Network')
    maintenance_centers = fields.Many2one('maintenance.center', 'Service Center')
    date = fields.Date('Intimation Date', default=datetime.today())
    declaration_ids = fields.One2many('claim.lines', 'opp_id')



    @api.onchange('policy')
    def get_policy(self):
        if self.policy:
            pol = self.env['policy.arope'].search([('product', '=', self.policy_seq.product_name),
                                                   ('policy_num', '=', int(self.policy))], limit=1)
            self.customer = self.env['persons'].search([('type', '=', 'customer'), ('pin', '=', pol.customer_pin)],
                                                       limit=1).name
            # self.agent_code = str(pol.pin)
            self.start_date = pol.inception_date
            self.end_date = pol.expiry_date

    end_reason = fields.Text(string='Endorsement Reason')
    cancel_reason = fields.Text(string='Cancel Reason')

    @api.onchange('offer_ids')
    def change_offer(self):
        if self.offer_ids:
            offers = []
            for rec in self.offer_ids:
                offers.append(rec)
            if offers[-1].offer_state == 'submitted':
                if offers[-1].type == 'initial':
                    self.stage_id = self.env['crm.stage'].search(
                        [('name', '=', 'Initial Offer'), ('type', '=', self.opp_type.id)]).id
                    self.message = self.stage_id.message
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
                    self.stage_id = self.env['crm.stage'].search(
                        [('name', '=', 'Issue In Progress'), ('type', '=', self.opp_type.id)]).id
                    self.message = self.stage_id.message
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



    @api.onchange('lob')
    def compute_application_number(self):
        if self.lob:
            number = self.env['ir.sequence'].next_by_code('application_number')
            currentYear = datetime.today().strftime("%Y")
            currentMonth = datetime.today().strftime("%m")
            self.write(
                {'application_number': self.lob.line_of_business.upper() + '/' + currentYear[2:4] + '/' + currentMonth +
                                       '/' + number})


    @api.onchange('product_id')
    def get_questions(self):
        # if self.survey_report_ids:
        #     for question in self.survey_report_ids:
        #         question.unlink()
        if self.question_ids:
            for question in self.question_ids:
                question.unlink()
        if self.product_id == 4 or self.product_id == 7:
            related_questions = self.env["questionnaire.lines.setup"].search([("product_id.id", "=", self.product_id.id)])
            if related_questions:
                for question in related_questions:
                        self.question_ids.create(
                            {"question": question.id, "choose_application_id": self.id})



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

    @api.onchange('stage_id')
    @api.constrains('stage_id')
    def change_stage_id(self):

        if self.stage_id.name == 'Survey':

            number = self.env['ir.sequence'].next_by_code('survies')
            currentYear = datetime.today().strftime("%Y")
            currentMonth = datetime.today().strftime("%m")

            survey = self.env['survey.report'].create(
                {"name": "Survey"+ '/' + currentYear[2:4] + '/' + currentMonth + '/' + number,
                 "type": 'insurance_application',
                 "request_id": self.id,'state': 'pending', 'status': self.env['state.setup'].search([('survey_status', '=', 'pending'),('type', '=', 'survey')]).id,
                 'message':self.env['state.setup'].search([('survey_status', '=', 'pending'),('type', '=', 'survey')]).message,
                 "lob": self.lob.id, 'product_id': self.product_id.id,"customer_name": self.customer_name, 'phone': self.phone, 'email': self.email,
                 'application_date': self.application_date})
            self.customer_name = survey.name
        if self.stage_id.name == 'Solved':
            self.customer_name = self.customer_name = self.env['crm.stage'].search([('name', '=', 'Survey'),
                                                          ('type', '=', self.opp_type.id)]).name
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'wizard.insurance.quotation',
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_request_id': self.id
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
    def get_survey(self):

        self.ensure_one()
        return {
            'name': 'Survey Report',
            'res_model': 'survey.report',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'domain': [('request_id', '=', self.id)],
            'context': {
                "create": False,
            },
        }

    @api.onchange('type','product','policy_num')
    def compute_claim_number(self):
        if self.opp_type and self.product and self.policy_num:
            number = self.env['ir.sequence'].next_by_code('claim_number')
            currentYear = datetime.today().strftime("%Y")
            currentMonth = datetime.today().strftime("%m")
            person = ''
            lob = ''
            self.write(
                {'claim_number': self.opp_type.upper() + '/' + self.claim_product.product_name + '/' + self.policy_num +
                    '/'+ currentYear + '/' + currentMonth + '/' + number})
            policy = self.env['policy.arope'].search(
                [('product', '=', self.claim_product.product_name), ('policy_num', '=', int(self.policy_num))
                 ], limit=1)
            for rec in self.env['insurance.line.business'].search([('line_of_business', '=', policy.lob)]):
                lob = rec.id

            for rec in self.env['persons'].search([('pin', '=', policy.customer_pin)]):
                person = rec
            if person != '' and lob != '':
                self.write({'lob': lob, 'customer_name': person.name, 'phone': person.mobile})
            elif lob == '':
                self.write({'customer_name': person.name, 'phone': person.mobile})
            else:
                self.write({'lob': lob})

    # @api.onchange('type')
    #claim
    def get_questions(self):
        # if self.type == 'motor':
        #     self.write({"state": self.env['state.setup'].search(
        #         [('claim_status', '=', 'claim_intimation'), ('type', '=', 'claim')]).id})
        #     self.write({"status": "claim_intimation"})
        #     self.write({"sub_state": "pending"})
        # else:
        #     self.write({"state": self.env['state.setup'].search(
        #         [('non_motor_claim_status', '=', 'claim_intimation'), ('type', '=', 'claim')]).id})
        #     self.write({"status": "claim_intimation"})
        #     self.write({"sub_state": "pending"})

        if self.declaration_ids:
            for question in self.declaration_ids:
                question.unlink()
        declaration_question = self.env["claim.setup.lines"].search([("claim_declaration_id", "=", self.env['claim.setup'].search([('type', '=', self.type)]).id),
                                                                     ('type', '=', 'claim_intimation')])
        if declaration_question:
            for question in declaration_question:
                if question.file:
                    self.declaration_ids.create(
                        {"question": question.id,'download_files': [question.file.id],
                         "claim_declaration_id": self.id})
                else:
                    self.declaration_ids.create(
                        {"question": question.id,"claim_declaration_id": self.id})

class CrmStages(models.Model):
    _inherit = "crm.stage"

    type = fields.Many2many('request.type',string='Type')
    message = fields.Text('Message', translate=True)
class RequestsTypes(models.Model):
    _name = "request.type"
    _rec_name = 'type'

    type = fields.Char(string='Request Type')