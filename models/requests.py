from datetime import timedelta, datetime
import base64
from xlrd import open_workbook
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo import api, tools, fields, models


class CrmLeads(models.Model):
    _inherit = "crm.lead"
