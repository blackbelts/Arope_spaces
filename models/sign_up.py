import logging

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError
from odoo.http import request

class ResUsers(models.Model):
    _inherit = 'res.users'

    x_pin = fields.Char(string='PIN')

    @api.model
    def _signup_create_user(self, values):
        values['x_pin'] = values.get('x_pin')
        new_user = super(ResUsers, self)._signup_create_user(values)
        if new_user:
            self.env['crm.lead'].create({
                'opp_type': 5,
                'customer_name': new_user.name,
                'email': new_user.login,
                'pin': new_user.x_pin
            })
        return new_user