from odoo import models, tools, fields, api,exceptions
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import timedelta, datetime,date
class AropePolicyRequests(models.Model):
    _name = "policy.request"
    _rec_name='name'

    @api.model
    def create(self, vals):
        serial_no = self.env['ir.sequence'].next_by_code('req')
        if vals.get('type') =='end':
           r_type='End'
        elif vals.get('type') =='renew':
           r_type='Renew'
        # merge code and serial number
        vals['name'] =  str(serial_no)+'/'+r_type

        return super(AropePolicyRequests, self).create(vals)

    name=fields.Char('Request')
    policy=fields.Integer('Policy Num')
    product=fields.Char('Policy Product')
    state = fields.Selection([('pending', 'Pending'),
                              ('submitted', 'Submitted'), ('issued', 'Issued')], 'State', default='pending')


    type =fields.Selection([('end', 'Endorsement'),
                                ('renew', 'Renwal')],string='Request Type')
    end_reason= fields.Text(string='Endorsement Reason')

    def submit(self):
        self.state='submitted'
    def issue(self):
        self.state='submitted'


class AropePolicy(models.Model):
    _inherit = "policy.arope"

    def create_end_requset(self):
        form = self.env.ref('arope-conf.request_form_view')

        return {
            'name': ('Request'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'policy.request',
            # 'view_id': [(self.env.ref('smart_claim.tree_insurance_claim').id), 'tree'],
            'views': [(form.id, 'form')],
            'type': 'ir.actions.act_window',
            'target': 'current',

            'context': {'default_type': 'end', 'default_policy': self.policy_num, 'default_product': self.product}

        }

    def create_renew_requset(self):
        form = self.env.ref('arope-conf.request_form_view')
        return {
            'name': ('Request'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'policy.request',
            # 'view_id': [(self.env.ref('smart_claim.tree_insurance_claim').id), 'tree'],
            'views': [(form.id, 'form')],
            'type': 'ir.actions.act_window',
            'target': 'current',

            'context': {'default_type': 'renew', 'default_policy': self.policy_num, 'default_product': self.product}

        }


