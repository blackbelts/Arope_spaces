from odoo import models, tools, fields, api,exceptions
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import timedelta, datetime,date
class HelpDeskComplains(models.Model):
    _inherit = 'helpdesk_lite.ticket'
    lob = fields.Many2one('insurance.line.business', 'LOB',)
    partner_id = fields.Many2one('persons',string='Customer',domain="[('is_customer', '=', True)]")
    card_id = fields.Char(related='partner_id.card_id',string='Customer')

    product = fields.Many2one('insurance.product', 'Product', domain="[('line_of_bus', '=', lob)]")
    def create_application(self):
        self.env['insurance.quotation'].create({'name': self.contact_name,
                                                'lob':self.lob.id,'product_id':self.product_id.id})
        print('Write Method')
