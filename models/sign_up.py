import logging

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError
from odoo.http import request

class ResUsers(models.Model):
    _inherit = 'res.users'

    x_pin = fields.Char(string='PIN')

    @api.model
    def _signup_create_user(self, values):

        new_user = super(ResUsers, self)._signup_create_user(values)
        if new_user:
            self.env['crm.lead'].create({
                'customer_name': new_user.name
            })
        return new_user