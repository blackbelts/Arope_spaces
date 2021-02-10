from datetime import timedelta, datetime
import base64
from xlrd import open_workbook
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo import api, tools, fields, models


class CrmLeads(models.Model):
    _inherit = "crm.lead"
    opp_type = fields.Selection([('insurance_app', 'Insurance Application'),
                                ('motor_claim', 'Motor Claim'),('general_claim', 'General Claim'),
                                 ('end', 'Endorsement'),('renew', 'Renewal'),('cancel', 'Cancellation'),
                                 ('quote','Quote'),('signup','Sign Up')],string='Type')
