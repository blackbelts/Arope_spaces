from odoo import models, fields, api
from odoo.exceptions import ValidationError




class InheritBrokers(models.Model):
    _inherit = 'persons'


    def view_dashboard(self):
        print('kkkkkkkkkkkkkkkkkk')

        # form = self.env.ref('Arope-spaces.brokers_user_wizard')
        # self.is_user = True
        action = self.env.ref('Arope-spaces.arope_action_dashboard').read()[0]
        return {'action':action,'id':6}
        # return {
        #     'name': ('Users'),
        #     'view_type': 'form',
        #     'view_mode': 'form',
        #     'res_model': 'broker.user.wizard',
        #     # 'view_id': [(self.env.ref('smart_claim.tree_insurance_claim').id), 'tree'],
        #     'views': [(form.id, 'form')],
        #     'type': 'ir.actions.act_window',
        #     'target': 'new',
        #
        #     'context': {'default_name': self.name,
        #                 'default_agent_code': self.agent_code,'default_card_id': self.card_id}
        #
        # }










