from odoo import models, tools, fields, api


class StateSetup(models.Model):
    _name = 'state.setup'
    _rec_name = 'state'

    status = fields.Selection([
        ('proposal', 'Request For Offer'),
        ('initial_offer', 'Initial Offer'),
        ('application_form', 'Application Form'),
        ('survey', 'Survey'),
        ('final_offer', 'Final Offer'),
        ('application', 'Issue In Progress'),
        ('policy', 'Policy Issued'),
        ('cancel', 'Lost')], string='State')
    claim_status = fields.Selection([('claim_intimation', 'Claim Intimation'),
                                     ('invoicing', 'Invoicing'),
                                     ('repair', 'Start Repair'),
                                     ('survey_after_repair', 'Confirm Repair'),
                                     ('total_loss', 'Total Loss'),
                                     ('cheque', 'Take Cheque'),
                                     ('car_release', 'Car Release')], string='State')
    state = fields.Char('State')
    type = fields.Selection([('insurance_app', 'Insurance Application'),
                             ('claim', 'Claim'), ('survey', 'Survey')], string='Type')
    survey_status = fields.Selection([('pending', 'Pending'), ('surveyor', 'Surveyor Assigned'),
                            ('submitted', 'Submitted'), ('accepted', 'Accepted')], 'State', default='pending')
    claim_type = fields.Selection([('motor', 'Motor'),('non-motor', 'Non Motor')], string="Claim Type")
    # lob = fields.Many2one('insurance.line.business', 'LOB', required=True)
    product_ids = fields.Many2many('insurance.product', string='Product')
    # state_for = fields.Selection([('broker', 'Broker'),
    #                               ('surveyor', 'Surveyor'),('underwriter', 'Underwriter')], string='State For')
    message = fields.Text('Message')

    @api.onchange('status', 'claim_status', 'survey_status')
    def compute_status(self):
        if self.status:
            self.state = dict(self._fields['status'].selection).get(self.status)
        elif self.claim_status:
            self.state = dict(self._fields['claim_status'].selection).get(self.claim_status)
        elif self.survey_status:
            self.state = dict(self._fields['survey_status'].selection).get(self.survey_status)





