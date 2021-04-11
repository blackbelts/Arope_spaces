from odoo import models, tools, fields, api


class StateSetup(models.Model):
    _name = 'state.setup'
    _rec_name = 'state'

    status = fields.Selection([
        ('application_form', 'Application Form'),
        ('initial_offer', 'Initial Offer'),
        ('survey', 'Survey'),
        ('final_offer', 'Final Offer'),
        ('application', 'Issue In Progress'),
        ('policy', 'Policy Issued'),
        ('cancel', 'Lost')], string='State' ,translate=True)
    claim_status = fields.Selection([('claim_intimation', 'Claim Intimation'),
                                     ('invoicing', 'Invoicing'),
                                     ('pre_survey', 'Pre Survey'),
                                     ('repair', 'Start Repair'),
                                     ('repair_completed', 'Repair Comleted'),
                                     ('survey_after_repair', 'Survey After Repair'),
                                     ('total_loss', 'Total Loss'),
                                     ('cheque', 'Take Cheque'),
                                     ('car_release', 'Car Release'),
                                     ('reject','Reject')], string='State' ,translate=True)

    non_motor_claim_status = fields.Selection([('claim_intimation', 'Claim Intimation'),
                                                ('pre_survey', 'Survey'),
                                                ('estimation', 'Estimation'),
                                               ('cheque', 'Cheque Ready'),
                                               ('reject', 'Reject')], string='State' ,translate=True)
    state = fields.Char('State' ,translate=True)
    type = fields.Selection([('insurance_app', 'Insurance Application'),
                             ('claim', 'Claim'), ('survey', 'Survey')], string='Type')
    survey_status = fields.Selection([('pending', 'Pending'), ('surveyor', 'Surveyor Assigned'),
                                      ('suspended', 'Suspended'),
                                        ('submitted', 'Submitted'), ('accepted', 'Accepted')], 'State', default='pending',translate=True)
    claim_type = fields.Selection([('motor', 'Motor'),('non-motor', 'Non Motor')], string="Claim Type",translate=True)
    # lob = fields.Many2one('insurance.line.business', 'LOB', required=True)
    product_ids = fields.Many2many('insurance.product', string='Product')
    # state_for = fields.Selection([('broker', 'Broker'),
    #                               ('surveyor', 'Surveyor'),('underwriter', 'Underwriter')], string='State For')
    message = fields.Text('Message',translate=True)

    @api.onchange('status', 'claim_status', 'survey_status')
    def compute_status(self):
        if self.status:
            self.state = dict(self._fields['status'].selection).get(self.status)
        elif self.claim_status:
            self.state = dict(self._fields['claim_status'].selection).get(self.claim_status)
        elif self.survey_status:
            self.state = dict(self._fields['survey_status'].selection).get(self.survey_status)
        # elif self.non_motor_claim_status:
        #     self.state = dict(self._fields['non_motor_claim_status'].selection).get(self.non_motor_claim_status)

    @api.onchange('non_motor_claim_status')
    def non_compute_status(self):
        if self.non_motor_claim_status:
            self.state = dict(self._fields['non_motor_claim_status'].selection).get(self.non_motor_claim_status)






