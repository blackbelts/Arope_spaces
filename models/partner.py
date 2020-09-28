from odoo import models, fields, api
from odoo.exceptions import ValidationError



class inhertResUser(models.Model):
    _inherit = 'res.users'

    is_broker = fields.Boolean(string='Broker',default=False)
    agent_code = fields.Char(string='Agent Code')
    card_id = fields.Char(string='Broker Card')

class InheritBrokers(models.Model):
    _name = 'persons'
    _rec_name='name'
    name=fields.Char(string='Broker Name')
    card_id = fields.Char(string='Card ID')
    com_reg = fields.Integer(string='Commerical Register')
    pin = fields.Integer(string='PIN')
    fra_no = fields.Char(string='FRA No')
    expire_date = fields.Date(string='Expiration Date')
    agent_code = fields.Char(string='Agent Code')
    mobile = fields.Char(string='Mobile')
    related_user=fields.Many2one('res.users',string='Persons User')
    is_user = fields.Boolean(string='User',default=False)
    type = fields.Selection([('broker', 'Broker'),
                                  ('surveyor', 'Surveyor'), ('customer', 'Customer')], default='broker' ,string='Type')





    def create_broker_user(self):
        form = self.env.ref('Arope-spaces.brokers_user_wizard')
        self.is_user = True
        return {
            'name': ('Users'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'broker.user.wizard',
            # 'view_id': [(self.env.ref('smart_claim.tree_insurance_claim').id), 'tree'],
            'views': [(form.id, 'form')],
            'type': 'ir.actions.act_window',
            'target': 'new',

            'context': {'default_name': self.name,
                        'default_agent_code': self.agent_code,'default_card_id': self.card_id}

        }










