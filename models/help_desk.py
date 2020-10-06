from odoo import models, tools, fields, api,exceptions
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import timedelta, datetime,date
class HelpDeskComplains(models.Model):
    _inherit = 'helpdesk_lite.ticket'
    lob = fields.Many2one('insurance.line.business', 'LOB',)
    customer = fields.Char(string='Customer')
    agent_code = fields.Char(string='Agent Code')
    card_id = fields.Char(string='Card ID')
    policy = fields.Char(string='Policy')
    policy_no = fields.Integer(string='Policy')

    product = fields.Many2one('insurance.product', 'Product', domain="[('line_of_bus', '=', lob)]")
    print('Write Method')

    @api.onchange('policy','policy_no')
    def get_policy(self):
        if self.policy and self.policy_no:
            pol=self.env['policy.arope'].search([('product','=', self.policy),('policy_num','=', self.policy_no)
                                                    ],limit=1)
            self.customer=str(pol.pin)
            self.agent_code=str(pol.pin)



class HelpDeskQuotes(models.Model):
    _inherit = 'quoate'
    lob = fields.Many2one('insurance.line.business', 'LOB',)
    product = fields.Many2one('insurance.product', 'Product', domain="[('line_of_bus', '=', lob)]")
    def create_application(self):
        self.env['insurance.quotation'].create({'name': self.contact_name,
                                                'lob':self.lob.id,'product_id':self.product_id.id,'phone':self.phone,
                                                'email':self.email_from})
        print('Write Method')
