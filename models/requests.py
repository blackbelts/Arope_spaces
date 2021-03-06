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
    # state_ids = fields.Many2one('crm.stage')
    message = fields.Text('Description')
    policy_services_type = fields.Selection([('end', 'Endorsement'),
                                ('renew', 'Renwal')],string='Request Type')
    cancel_reason = fields.Text('Cancel Reason')

    def cancel(self):
        self.stage_id = self.env['crm.stage'].search(
            [('name', '=', 'Closed'), ('type', '=', self.opp_type.id)]).id
        self.message = self.stage_id.message

    # @api.onchange('stage_id')
    @api.onchange('opp_type')
    @api.constrains('opp_type')
    def stage_domain(self):
        if self.stage_id:
            self.message = self.stage_id.message
        if self.opp_type.id == 3 or self.opp_type.id == 4:
            if self.opp_type.id == 3:
                name = 'non-motor'
            elif self.opp_type.id == 4:
                name = 'motor'
            if self.declaration_ids:
                for question in self.declaration_ids:
                    question.unlink()
            declaration_question = self.env["claim.setup.lines"].search(
                [("claim_declaration_id", "=", self.env['claim.setup'].search([('type', '=', name)]).id),
                 ('type', '=', 'claim_intimation')])
            # if declaration_question:
            for question in declaration_question:
                    if question.file:
                        self.declaration_ids.create(
                            {"question": question.id, 'download_files': [question.file.id],
                             "opp_id": self.id})
                    else:
                        self.declaration_ids.create(
                            {"question": question.id, "opp_id": self.id})

        return {'domain': {'stage_id': [('type', 'in', self.opp_type.id)]}}

    customer_name = fields.Char('Customer Name')
    phone = fields.Char('Customer Mobile')
    email = fields.Char('Customer Email')
    isClickable = fields.Boolean(string='is clickable')
    user_click = fields.Many2one('res.users', 'User Name', index=True, track_visibility='onchange',
                              compute='current_user', store=False ,readonly=True)
    user_test = fields.Many2one('res.users')
    application_number = fields.Char(string='Application Number', copy=False, index=True)
    application_date = fields.Date('Application Date', default=datetime.today(), readonly=True)
    policy_number = fields.Char('Policy Num')
    policy_issue_date = fields.Date('Policy Issue Date')
    name_of_contact_person = fields.Char('Survey Contact Person')
    main_phone = fields.Char('Mobile Number (Main)')
    spare_phone = fields.Char('Mobile Number (Spare)')

    offer_state = fields.Selection([('accepted', 'Accepted'),('rejected', 'Rejected')], string="Offer State", readonly=True)
    persons = fields.One2many('persons.lines', 'opp_id')
    offer_ids = fields.One2many('final.offers', 'opp_id')
    question_ids = fields.One2many('insurances.answers', 'request_id')
    name = fields.Char('Request')
    agent_code = fields.Char('Agent Code')
    recomm = fields.Text('Recommendation')
    notes_recommendations = fields.Many2many('ir.attachment', string="Notes or Recommendations", relation="notes_recommendations")
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
    pin = fields.Char('PIN')
    financial_clearance = fields.Many2many('ir.attachment', string="Financial Clearance" , relation="financial_clearance")
    attach_policy = fields.Binary(string='Policy Attachment')
    #Online Quote
    contact_name = fields.Char('Contact Name')
    email_from = fields.Char('Email', help="Email address of the contact", index=True)
    job = fields.Char('Job')
    phone = fields.Char('Phone')
    ticket_type = fields.Selection([('personal', 'PA'),
                                    ('travel', 'Travel'), ('medical', 'Medical'), ('motor', 'Motor')],
                                   default='personal')
    sum_insured = fields.Float('Sum Insured')
    state = fields.Selection([('new', 'New'),
                              ('verified', 'Verified'),
                              ('proposal', 'Proposal'),
                              ('won', 'Won'),
                              ('canceled', 'Canceled'), ],
                             'Status', required=True, default='new', copy=False)

    user_id = fields.Many2one('res.users', string='Assigned to', track_visibility='onchange', index=True, default=False,
                              )

    active = fields.Boolean(default=True)
    offer = fields.Many2many('ir.attachment', string="Offer", relation="offer")
    offer_validation_start = fields.Date('Offer Validation Start From')
    offer_validation_end = fields.Date('To')
    source = fields.Selection([('online', 'Online'),
                               ('call', 'Call Center'),
                               ('social', 'Social Media')],
                              'Source', copy=False)

    support_team = fields.Many2one('helpdesk_lite.team', string='Team')

    # Complains

    # username = fields.Char('UserName')
    # password = fields.Char('Password')
    # phone = fields.Char('Mobile Number')
    complain = fields.Text('Complain')
    source = fields.Selection([('online', 'Online'),
                               ('call', 'Call Center'),
                               ('social', 'Social Media')],
                              'Source', copy=False)

    # team_id = fields.Many2one('helpdesk_lite.team', string='Complaint Types', index=True)

    @api.onchange('policy')
    @api.constrains('policy')
    def get_policy(self):
        if self.policy:
            pol = self.env['policy.arope'].search([('product', '=', self.policy_seq.product_name),
                                                   ('policy_num', '=', int(self.policy))], limit=1)
            self.customer = self.env['persons'].search([('type', '=', 'customer'), ('pin', '=', pol.customer_pin)],
                                                       limit=1).name
            # self.agent_code = str(pol.pin)
            self.start_date = pol.inception_date
            self.end_date = pol.expiry_date
            self.agent_code = pol.agent_code

    end_reason = fields.Text(string='Endorsement Reason')
    cancel_reason = fields.Text(string='Cancel Reason')

        # res = {}
        # for i in self.browse(cr, uid, ids, context=context):
        #     res[i.clickable] = 'odedra'
        # return res
    @api.depends('user_test')
    def get_group_security(self):
        # for rec in self:
        if self.env.user.has_group('Arope_spaces.broker_space_group'):
            self.isClickable = False
        else:
            self.isClickable = True


    @api.onchange('offer')
    def change_offers(self):
        if self.offer:
            # offers = []
            # for rec in self.offer_ids:
            #     offers.append(rec)
            # if offers[-1].offer_state == 'submitted':
            #     if offers[-1].type == 'initial':
            self.stage_id = self.env['crm.stage'].search(
                [('name', '=', 'Offer Ready'), ('type', '=', self.opp_type.id)]).id
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

            # elif offers[-1].offer_state == 'accepted':
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
                # if offers[-1].type == 'final':
                #     self.stage_id = self.env['crm.stage'].search(
                #         [('name', '=', 'Issue In Progress'), ('type', '=', self.opp_type.id)]).id
                #     self.message = self.stage_id.message
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


    # @api.onchange('product_id')
    # def get_questions(self):
        # if self.survey_report_ids:
        #     for question in self.survey_report_ids:
        #         question.unlink()

        # if self.question_ids:
        #     for question in self.question_ids:
        #         question.unlink()
        # if self.product_id == 4 or self.product_id == 7:
        #     related_questions = self.env["questionnaire.lines.setup"].search([("product_id.id", "=", self.product_id.id)])
        #     if related_questions:
        #         for question in related_questions:
        #                 self.question_ids.create(
        #                     {"question": question.id, "choose_application_id": self.id})



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
        # self.state_ids = self.stage_id.id
        if self.stage_id.name == 'Survey' and self.opp_type.id == 1:

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
            # self.customer_name = survey.name
        elif self.stage_id.name == 'Repair, Upload Invoices' and self.opp_type.id == 4:
            declaration_question = self.env["claim.setup.lines"].search(
                [("claim_declaration_id", "=", self.env['claim.setup'].search([('type', '=', 'motor')]).id),
                 ('type', '=', 'invoicing')])
            if declaration_question:
                for question in declaration_question:
                    if question.file:
                        self.declaration_ids.create(
                            {"question": question.id, 'download_files': [question.file.id],
                             "opp_id": self.id})
                    else:
                        self.declaration_ids.create(
                            {"question": question.id, "opp_id": self.id})

        elif self.stage_id.name == 'Survey' and self.opp_type.id == 3:
            number = self.env['ir.sequence'].next_by_code('survies')
            currentYear = datetime.today().strftime("%Y")
            currentMonth = datetime.today().strftime("%m")
            person = ''
            policy = self.env['policy.arope'].search(
                [('product', '=', self.product), ('policy_num', '=', int(self.policy_num))
                 ], limit=1)
            for rec in self.env['insurance.line.business'].search([('line_of_business', '=', policy.lob)]):
                lob = rec.id
            for rec in self.env['insurance.product'].search([('product_name', '=', policy.product)]):
                product = rec.id
            for rec in self.env['persons'].search([('pin', '=', policy.customer_pin)]):
                person = rec
            if person != '':
                type = 'non_motor_claim'
                survey_type = 'pre_survey'
                self.env['survey.report'].create(
                    {"name": "Survey" + '/' + currentYear[2:4] + '/' + currentMonth + '/' + number,
                     "type": type, 'survey_type': survey_type,
                     "request_id": self.id, 'state': 'pending',
                     'status': self.env['state.setup'].search(
                         [('survey_status', '=', 'pending'), ('type', '=', 'survey')]).id,
                     'message': self.env['state.setup'].search(
                         [('survey_status', '=', 'pending'), ('type', '=', 'survey')]).message,
                     "lob": lob, 'product_id': product, "customer_name": person.name, 'phone': person.mobile
                     })
        elif self.opp_type.id == 4:
            if self.stage_id.name == 'Pre Repair Assessment' or self.stage_id.name == 'Post Repair Assessment':
                if self.stage_id.name == 'Pre Repair Assessment':
                    type = 'motor_claim'
                    survey_type = 'pre_survey'
                elif self.stage_id.name == 'Post Repair Assessment':
                    type = 'motor_claim'
                    survey_type = 'Survey_after_repair'

                number = self.env['ir.sequence'].next_by_code('survies')
                currentYear = datetime.today().strftime("%Y")
                currentMonth = datetime.today().strftime("%m")
                person = ''
                policy = self.env['policy.arope'].search(
                    [('product', '=', self.product), ('policy_num', '=', int(self.policy_num))
                     ], limit=1)
                for rec in self.env['insurance.line.business'].search([('line_of_business', '=', policy.lob)]):
                    lob = rec.id
                for rec in self.env['insurance.product'].search([('product_name', '=', policy.product)]):
                    product = rec.id
                for rec in self.env['persons'].search([('pin', '=', policy.customer_pin)]):
                    person = rec
                if person != '':
                    self.env['survey.report'].create(
                        {"name": "Survey" + '/' + currentYear[2:4] + '/' + currentMonth + '/' + number,
                         "type": type, 'survey_type': survey_type,
                         "request_id": self.id, 'state': 'pending',
                         'status': self.env['state.setup'].search(
                             [('survey_status', '=', 'pending'), ('type', '=', 'survey')]).id,
                         'message': self.env['state.setup'].search(
                             [('survey_status', '=', 'pending'), ('type', '=', 'survey')]).message,
                         "lob": lob, 'product_id': product, "customer_name": person.name, 'phone': person.mobile
                         })
        # elif self.stage_id.name == 'Submitted':
        #     if self.lob:
        #        mail =  self.env['helpdesk_lite.team'].search([('lob', 'in', self.lob.id),('request_type', 'in', self.opp_type.id)]).team_mail
        #     else:
        #         mail = self.env['helpdesk_lite.team'].search([('lob', '=', False),('request_type', 'in', self.opp_type.id)]).team_mail
        #     if mail:
        #         self.ensure_one()
        #         ir_model_data = self.env['ir.model.data']
        #         template_id = self.env.ref('Arope_spaces.email_template')
        #         template_id.write({'email_to': mail})

                # template_id.send_mail(self.ids[0], force_send=True)

    def issued(self):
        self.stage_id = self.env['crm.stage'].search(
            [('name', '=', 'Issued'), ('type', '=', self.opp_type.id)]).id
        # self.message = self.stage_id.message
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
    @api.constrains('type', 'product', 'policy_num')
    def compute_claim_number(self):
        if self.opp_type and self.product and self.policy_num:
            number = self.env['ir.sequence'].next_by_code('claim_number')
            currentYear = datetime.today().strftime("%Y")
            currentMonth = datetime.today().strftime("%m")
            person = ''
            lob = ''
            self.write(
                {'claim_number': 'GENERAL' + '/' + self.product + '/' + self.policy_num +
                    '/'+ currentYear + '/' + currentMonth + '/' + number})
            policy = self.env['policy.arope'].search(
                [('product', '=', self.product), ('policy_num', '=', int(self.policy_num))
                 ], limit=1)
            for rec in self.env['insurance.line.business'].search([('line_of_business', '=', policy.lob)]):
                lob = rec.id

            for rec in self.env['persons'].search([('pin', '=', policy.customer_pin)]):
                person = rec
            if person != '' and lob != '':
                self.write({'lob': lob, 'customer_name': person.name, 'phone': person.mobile, 'agent_code': policy.agent_code})
            elif lob == '':
                self.write({'customer_name': person.name, 'phone': person.mobile, 'agent_code': policy.agent_code})
            else:
                self.write({'lob': lob, 'agent_code': policy.agent_code})

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

    def related_policy(self):
        policy = self.env['policy.arope'].search([('product', '=', self.product), ('policy_num', '=', int(self.policy_num))
                                                   ], limit=1)
        self.ensure_one()
        return {
            'name': 'Related Policy',
            'res_model': 'policy.arope',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree',
            'domain': [('id', '=', policy.id)],
            'context': {
                "create": False,
            },
        }

    def submit(self):
        self.stage_id = self.env['crm.stage'].search(
            [('name', '=', 'Submitted'), ('type', '=', self.opp_type.id)]).id
        self.message = self.stage_id.message

    def accept_offer(self):
        offers = []
        for record in self.offer_ids:
            offers.append(record)
        offers[-1].offer_state = 'accepted'

    @api.onchange('offer_ids')
    def offer_type(self):
        offers = []
        supmit = []
        for record in self.offer_ids:
            offers.append(record)
        if len(offers) != 0:
            supmit.append(offers[-1])
            del offers[-1]
            for rec in offers:
                rec.types = 'initial'
            if supmit[-1].offer_state == 'submitted':
                self.stage_id = self.env['crm.stage'].search(
                    [('name', '=', 'Offer Ready'), ('type', '=', self.opp_type.id)]).id
                self.message = self.stage_id.message
        else:
            self.stage_id = self.env['crm.stage'].search(
                [('name', '=', 'Submitted'), ('type', '=', self.opp_type.id)]).id
            self.message = self.stage_id.message

    def survey(self):
        self.stage_id = self.env['crm.stage'].search(
            [('name', '=', 'Survey'), ('type', '=', self.opp_type.id)]).id
        self.message = self.stage_id.message

    def issue_in_progress(self):
        self.stage_id = self.env['crm.stage'].search(
            [('name', '=', 'Issue In Progress'), ('type', '=', self.opp_type.id)]).id
        self.message = self.stage_id.message

    def offer(self):
        self.stage_id = self.env['crm.stage'].search(
            [('name', '=', 'Offer Ready'), ('type', '=', self.opp_type.id)]).id
        self.message = self.stage_id.message



    #Online Quote
    def current_user(self):
        self.user_click = self.env.uid
        self.user_test = self.env.uid
        if self.env.user.has_group('Arope_spaces.broker_space_group'):
            self.isClickable = False
        else:
            self.isClickable = True


    def takeit(self):
        self.user_id = self.env.uid


    @api.onchange('support_team')
    def onchange_support_team(self):
        if self.support_team:
            # filter products by seller
            user_ids = self.support_team.member_ids.ids
            return {'domain': {'user_id': [('id', 'in', user_ids)]}}
        else:
            # filter all products -> remove domain
            return {'domain': {'user_id': []}}

class CrmStages(models.Model):
    _inherit = "crm.stage"

    type = fields.Many2many('request.type',string='Type')
    message = fields.Text('Message', translate=True)
class RequestsTypes(models.Model):
    _name = "request.type"
    _rec_name = 'type'

    type = fields.Char(string='Request Type', readonly=True)




class TicketTypes(models.Model):
    _inherit = 'helpdesk_lite.team'
    support_chain = fields.Many2many('res.users', string='Support Chain')
    team_support_type = fields.Selection([('personal', 'PA'),
                                          ('travel', 'Travel'), ('medical', 'Medical'), ('motor', 'Motor')],
                                         default='personal', sting='Support Type')
    request_type = fields.Many2many('request.type', sting='request Type')
    lob = fields.Many2many('insurance.line.business', string='LOB')
    team_mail = fields.Char('Team Mail')



