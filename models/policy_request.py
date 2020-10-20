from odoo import models, tools, fields, api,exceptions
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import timedelta, datetime,date



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


