from odoo import api, fields, models
from datetime import datetime

class AropeClaim(models.Model):
    _name="claim.app"

    type = fields.Selection([('motor', 'Motor'),('non-motor', 'Non Motor')], string="Type")
    # name = fields.Char('Customer Name', required=True)
    product = fields.Many2one('insurance.product', 'Product')
    policy_num = fields.Char(string="Policy Number", copy=True)
    # car_num = fields.Char(string="Plate No", copy=True)
    chasse_num = fields.Char(string="Chasse No", copy=True)
    state = fields.Many2one('state.setup', domain="[('type', '=', 'claim'),('claim_type', '=', type)]")
    sub_state = fields.Selection([('pending', 'Pending'), ('initial_invoice', 'Initial Invoice'),
                                  ('invoice_details', 'Invoice Details'),('surveyor', 'Assign Surveyor'),
                                  ('survey', 'Survey'),('complete', 'Complete')], string="Sub State", readonly=True)
    maintenance_centers_in_or_out = fields.Selection([('in', 'Arope Network'), ('out', 'Outside Arope Network')], string='Service Center Network')
    maintenance_centers = fields.Many2one('maintenance.center', 'Service Center')
    date = fields.Date('Intimation Date', default=datetime.today())
    surveyor = fields.Many2one('res.users', 'Surveyor')
    survey_date = fields.Datetime('Appointment')
    second_surveyor = fields.Many2one('res.users', 'Surveyor')
    second_survey_date = fields.Datetime('Appointment')
    comment = fields.Text('Comment')
    recommendation = fields.Text('Recommendation')
    declaration_ids = fields.One2many('claim.lines', 'claim_declaration_id')
    # invoice_ids = fields.One2many('claim.lines', 'claim_invoice_id')
    # survey_ids = fields.One2many('claim.lines', 'claim_survey_id')
    status = fields.Selection([('claim_intimation', 'Claim Intimation'),
                                     ('invoicing', 'First Invoicing'),
                                     ('repair', 'Start Repair'),
                                     ('survey_after_repair', 'Confirm Repair'),
                                     ('total_loss', 'Total Loss'),
                                     ('cheque', 'Take Cheque'),
                                     ('car_release', 'Car Release'),
                                    ('reject','Reject')], string='State')
    total_invoice = fields.Float('Total Invoice')
    initial_invoice = fields.Many2many('ir.attachment', string="Upload Initial Invoice",relation="claim_app_initial_invoice")
    invoice_detail = fields.Many2many('ir.attachment', string="Upload Invoice Details", relation="claim_app_invoice_details")
    total_initial_invoice = fields.Float('Total Initial Invoice')
    survey_report = fields.Many2many('ir.attachment', string="Upload Survey Report", relation="claim_app_survey_report")

    # @api.onchange('state')
    # def compute_status(self):
    #     self.write({"status": self.state.claim_status})
    #     self.write({"sub_state": "pending"})



    @api.onchange('type')
    def get_questions(self):
        self.write({"state": self.env['state.setup'].search(
            [('claim_status', '=', 'claim_intimation'), ('type', '=', 'claim')]).id})
        self.write({"status": "claim_intimation"})
        self.write({"sub_state": "pending"})
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

    def complete_and_proceed(self):
        if self.status == 'claim_intimation':
            self.write({"state": self.env['state.setup'].search(
                [('claim_status', '=', 'invoicing'), ('type', '=', 'claim')]).id})
            self.write({"status": "invoicing"})
            self.write({"sub_state": "initial_invoice"})
            declaration_question = self.env["claim.setup.lines"].search(
                [("claim_declaration_id", "=", self.env['claim.setup'].search([('type', '=', self.type)]).id),
                 ('type', '=', 'invoicing')])
            if declaration_question:
                for question in declaration_question:
                    if question.file:
                        self.declaration_ids.create(
                            {"question": question.id, 'download_files': [question.file.id],
                             "claim_declaration_id": self.id})
                    else:
                        self.declaration_ids.create(
                            {"question": question.id, "claim_declaration_id": self.id})

        elif self.status == 'surveyor':
            self.write({"state": self.env['state.setup'].search(
                [('claim_status', '=', 'survey'), ('type', '=', 'claim')]).id})
            self.write({"status": "survey"})
            self.write({"sub_state": "pending"})
        elif self.status == 'repair':
            self.write({"state": self.env['state.setup'].search(
                [('claim_status', '=', 'survey_after_repair'), ('type', '=', 'claim')]).id})
            self.write({"status": "survey_after_repair"})
            self.write({"sub_state": "pending"})
        else:
            self.write({'sub_state': 'complete'})

    def invoice_details(self):
        self.write({"sub_state": "invoice_details"})


    def start_repair(self):
        self.write({"state": self.env['state.setup'].search(
            [('claim_status', '=', 'repair'), ('type', '=', 'claim')]).id})
        self.write({"status": "repair"})
        self.write({"sub_state": "pending"})

    def assign_surveyor(self):
        self.write({"sub_state": "surveyor"})

    def survey_report(self):
        self.write({"sub_state": "survey"})
        number = self.env['ir.sequence'].next_by_code('survies')
        currentYear = datetime.today().strftime("%Y")
        currentMonth = datetime.today().strftime("%m")
        policy = self.env['policy.arope'].search([('product', '=', self.product.product_name), ('policy_num', '=', int(self.policy_num))
                                                   ], limit=1)
        if self.type == 'motor':
            type = 'motor_claim'
            survey_type = 'pre_survey'

        else:
            type = 'non_motor_claim'
            survey_type = 'pre_survey'
        for rec in self.env['insurance.line.business'].search([('line_of_business', '=', policy.lob)]):
            lob = rec.id
        for rec in self.env['insurance.product'].search([('product_name', '=', policy.product)]):
            product = rec.id
        for rec in self.env['persons'].search([('customer_pin', '=', policy.pin)]):
            person = rec


        self.env['survey.report'].create(
            {"name": "Survey" + '/' + currentYear[2:4] + '/' + currentMonth + '/' + number,
             "type": type, 'survey_type': survey_type,
             "claim_id": self.id, 'state': 'pending',
             'status': self.env['state.setup'].search([('survey_status', '=', 'pending'), ('type', '=', 'survey')]).id,
             'message': self.env['state.setup'].search(
                 [('survey_status', '=', 'pending'), ('type', '=', 'survey')]).message,
             "lob": lob, 'product_id': product, "customer_name": person.name, 'phone': person.mobile
             })

    def total_loss(self):
        self.write({"state": self.env['state.setup'].search(
            [('claim_status', '=', 'total_loss'), ('type', '=', 'claim')]).id})
        self.write({"status": "total_loss"})
        self.write({"sub_state": "complete"})

    def take_cheque(self):
        self.write({"state": self.env['state.setup'].search(
            [('claim_status', '=', 'cheque'), ('type', '=', 'claim')]).id})
        self.write({"status": "cheque"})
        self.write({"sub_state": "complete"})

    def car_release(self):
        self.write({"state": self.env['state.setup'].search(
            [('claim_status', '=', 'car_release'), ('type', '=', 'claim')]).id})
        self.write({"status": "car_release"})
        self.write({"sub_state": "complete"})

    def get_survey(self):
        self.ensure_one()
        return {
            'name': 'Survey Report',
            'res_model': 'survey.report',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'domain': [('claim_id', '=', self.id)],
            'context': {
                "create": False,
            },
        }

    def related_policy(self):
        policy = self.env['policy.arope'].search([('product', '=', self.product.product_name), ('policy_num', '=', int(self.policy_num))
                                                   ], limit=1)
        self.ensure_one()
        return {
            'name': 'Related Policy',
            'res_model': 'policy.arope',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'domain': [('id', '=', policy.id)],
            'context': {
                "create": False,
            },
        }

class MaintenanceCenter(models.Model):
    _name = 'maintenance.center'
    _rec_name = 'name'
    name = fields.Char('Name')

class ClaimSetup(models.Model):

    _name = 'claim.setup'
    _rec_name = 'type'
    type = fields.Selection([('motor', 'Motor'), ('non-motor', 'Non Motor')], string="Type")
    claim_declaration_lines = fields.One2many('claim.setup.lines', 'claim_declaration_id', string='Claim Setup')


class ClaimDeclarationLines(models.Model):

    _name = 'claim.setup.lines'
    _rec_name = 'question'
    question = fields.Char('Document Name')
    file = fields.Many2many('ir.attachment', string="File")
    type = fields.Selection([('claim_intimation', 'Claim Intimation'),
                                     ('invoicing', 'First Invoicing')], string='State')
    claim_declaration_id = fields.Many2one('claim.setup', ondelele='cascade')


class ClaimLines(models.Model):
    _name = 'claim.lines'

    question = fields.Many2one('claim.setup.lines', 'Document Name')
    # text = fields.Text('Answer')
    download_files = fields.Many2many('ir.attachment', string="Download File")
    file = fields.Many2many('ir.attachment', string="Upload File", relation="claim_lines_uploads")
    claim_declaration_id = fields.Many2one('claim.app', ondelete='cascade')
    state = fields.Selection(
        [('pending', 'Pending'), ('complete', 'Submitted'), ('accepted', 'Accepted'), ('cancel', 'Rejected')],
        string='State', default='pending')
    comment = fields.Text('Comment')

    @api.onchange('file')
    def change_state(self):
        if self.file:
            self.write({"state": 'complete'})
    # claim_invoice_id = fields.Many2one('claim.app', ondelete='cascade')
    # claim_survey_id = fields.Many2one('claim.app', ondelete='cascade')





