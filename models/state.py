from odoo import models, tools, fields, api


class StateSetup(models.Model):
    _name = 'state.setup'
    _rec_name = 'state'

    status = fields.Selection([
        ('quick_quote', 'Quick Quote'),
        ('proposal', 'Request For Offer'),
        ('survey', 'Survey'),
        ('offer', 'Offering'),
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
                             ('claim', 'Claim')], string='Type')
    claim_type = fields.Selection([('motor', 'Motor'),('non-motor', 'Non Motor')], string="Claim Type")
    # lob = fields.Many2one('insurance.line.business', 'LOB', required=True)
    product_ids = fields.Many2many('insurance.product', string='Product')
    state_for = fields.Selection([('broker', 'Broker'),
                                  ('surveyor', 'Surveyor'),('underwriter', 'Underwriter')], string='State For')
    message = fields.Text('Message')

    @api.onchange('status', 'claim_status')
    def compute_status(self):
        if self.status:
            self.state = dict(self._fields['status'].selection).get(self.status)
        elif self.claim_status:
            self.state = dict(self._fields['claim_status'].selection).get(self.claim_status)

    @api.model
    def get_app_info(self, id):
        return id
        # status = []
        # rec = self.env['insurance.quotation'].search_read([('id', '=', id)])
        # for record in self.env['state.setup'].search([('product_ids', 'in', [rec[0].product_id.id]),
        #                                               ('type', '=', 'insurance_app'),
        #                                               ('state_for', '=', 'broker')]):
        #     status.append({"name": record.state, "message": record.message})
        # return {'status': status, 'app': rec}




