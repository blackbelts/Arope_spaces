from odoo import models, tools, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import timedelta, datetime

class Product(models.Model):
    _inherit = 'insurance.product'
    #

    # questionnaire_ids = fields.One2many('questionnaire.line.setup', 'product_id')
    survey_ids = fields.One2many('survey.line.setup', 'product_id')
    final_application_ids = fields.One2many('final.application.setup', 'product_id')
    # offer_setup_ids = fields.One2many('offer.setup', 'product_id')
    # state_id = fields.Many2one('state.setup', ondelete='cascade')

