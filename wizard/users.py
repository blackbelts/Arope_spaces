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

    def generate_broker_users(self):
        self.env['res.users'].create(
            {'name': self.name, 'login': self.name, 'password':self.password, 'agent_code': self.agent_code,
             'is_broker': True, 'groups_id': [
                self.env['res.groups'].search([('name', '=', 'Broker')]).id]})