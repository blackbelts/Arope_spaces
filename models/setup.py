from odoo import models, tools, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import timedelta, datetime


class Aropelinebusiness(models.Model):
    _name = "insurance.line.business"
    _rec_name = 'line_of_business'
    line_of_business = fields.Char(string='Line of Business', required=True)
    object = fields.Selection([('person', 'Person'),
                               ('vehicle', 'Vehicle'),
                               ('cargo', 'Cargo'),
                               ('location', 'Location'),
                               ('Project', 'Project')],
                              'Insured Type', track_visibility='onchange', required=True)
    desc = fields.Char(string='Description')
    product_ids=fields.One2many('insurance.product','line_of_bus',string='Products')


class Product(models.Model):
    _name = 'insurance.product'
    _rec_name = 'product_name'

    product_name = fields.Char('Product Name', required=True)
    line_of_bus = fields.Many2one('insurance.line.business', 'Line of Business',required=True)
    _sql_constraints = [
        ('product_unique', 'unique(product_name,line_of_bus)', 'Product already exists!')]




