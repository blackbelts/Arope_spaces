from datetime import timedelta, datetime
import base64
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo import api, fields, models

class AgentUsersWizard(models.TransientModel):
    _name = 'broker.user.wizard'

    name = fields.Char('Name')
    username = fields.Char('User Name')
    password = fields.Char('Password')
    agent_code = fields.Char(string='Agent Code')
    card_id = fields.Char(string='Broker Code')


    def generate_broker_users(self):
        context = self.env.context
        record = self.env[context['active_model']].browse(
            context['active_id'])
        if context['active_model'] == 'persons':
            person = record

        user=self.env['res.users'].create(
            {'name': self.name, 'login':self.card_id, 'password':self.password, 'agent_code': self.agent_code,
             'card_id': self.card_id,'related_person':person.id,
              'groups_id': [
                self.env['res.groups'].search([('name', '=', 'Broker')]).id]})
        person.write({'related_user':user.id})