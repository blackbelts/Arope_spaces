from odoo import models, tools, fields, api


class StateSetup(models.Model):
    _name = 'state.setup'
    _rec_name = 'state'
    status = fields.Selection([
        ('quick_quote', 'Quote'),
        ('proposal', 'Fill Form'),
        ('submitted', 'Form Complete'),
        ('survey_required', 'Survey Required'),
        ('surveyor', 'Surveyor Assigned'),
        ('survey', 'Survey Report'),
        ('survey_complete', 'Survey Complete'),
        ('reinsurance', 'Reinsurance'),
        ('offer', 'To Offer'),
        ('offer_ready', 'Offer Ready'),
        ('application', 'Upload Documents'),
        ('policy_pending', 'Policy Pending'),
        ('issued', 'Issued'),
        ('cancel', 'Rejected')], string='State')
    state = fields.Char('State')
    # lob = fields.Many2one('insurance.line.business', 'LOB', required=True)
    product_ids = fields.Many2many('insurance.product', string='Product')

    @api.onchange('status')
    def compute_status(self):
        self.state = dict(self._fields['status'].selection).get(self.status)


