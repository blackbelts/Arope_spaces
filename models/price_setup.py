from odoo import models, tools, fields, api

class QuotationPriceSetup(models.Model):
    _name = 'quotation.price.setup'
    _description = 'Set up Price tables'
    package = fields.Selection([('individual', 'Individual'),
                             ('family', 'Family'),],
                            'Package For',
                            default='individual')

    zone = fields.Selection([('zone 1', 'Europe'),
                                              ('zone 2', 'Worldwide excluding USA & CANADA'),
                                              ('zone 3', 'Worldwide'), ],
                                             'Zone',
                                             default='zone 1')
    currency_id=fields.Many2one('res.currency')
    from_age = fields.Float('From Age')
    to_age = fields.Float('To Age')

    price_lines=fields.One2many('quotation.price.line','price_id',string='Prices')

class QuotationPriceLine(models.Model):
    _name = 'quotation.price.line'

    period = fields.Integer('Period')
    issue_fees = fields.Float('Issue Fees')
    net_premium = fields.Float('Net Premium')
    proportional_stamp = fields.Float('Proportional Stamp')
    policy_approval_fees = fields.Float('Policy approval fees ')
    policy_holder_fees = fields.Float('Policyholder’s protection fees ')
    dimensional_stamp = fields.Float('Dimensional Stamp')
    supervisory_stamp = fields.Float('Supervisory Stamp')
    gross_premium = fields.Float('Gross Premium')
    price_id=fields.Many2one('quotation.price.setup', ondelete='cascade')