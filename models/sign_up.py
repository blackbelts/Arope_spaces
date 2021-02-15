import logging

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError
from odoo.http import request

class ResUsers(models.Model):
    _inherit = 'res.users'

    pin = fields.Char(string='PIN')

    # @api.model
    # def _signup_create_user(self, values):
    #     current_website = self.env['website'].get_current_website()
    #     if request and current_website.specific_user_account:
    #         values['company_id'] = current_website.company_id.id
    #         values['company_ids'] = [(4, current_website.company_id.id)]
    #         values['website_id'] = current_website.id
    #     new_user = super(ResUsers, self)._signup_create_user(values)
    #     return new_user