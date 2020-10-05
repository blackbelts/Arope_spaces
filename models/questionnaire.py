from odoo import models, tools, fields, api


class QuestionnaireLineSetup(models.Model):
    _name = 'questionnaire.line.setup'
    _rec_name= 'question'
    question = fields.Char('Question')
    options = fields.Many2many('selection.options', sting="Selections")
    desc = fields.Char('Description')
    question_type = fields.Selection([('text', 'Text'), ('numerical', 'Numerical'), ('choose', 'Choose')],
                                     'Question Type', default='text')

    product_id = fields.Many2one('insurance.product', ondelele='cascade', index=True)
    sub_questionnaire_id = fields.Many2one('sub.questionnaire', ondelele='cascade', index=True)


class SurveyLineSetup(models.Model):
    _name = 'survey.line.setup'
    _rec_name = 'question'
    question = fields.Char('Question')
    options = fields.Many2many('selection.options', sting="Selections")

    desc = fields.Char('Description')
    product_id = fields.Many2one('insurance.product', ondelele='cascade', index=True)

class FinalApplicationSetup(models.Model):
    _name = 'final.application.setup'
    _rec_name = 'description'
    description = fields.Char('Document Name')
    product_id = fields.Many2one('insurance.product', ondelele='cascade', index=True)

class OfferSetup(models.Model):
    _name = 'offer.setup'
    _rec_name = 'offer'
    offer = fields.Char('Offer Item')
    product_id = fields.Many2one('insurance.product', ondelele='cascade', index=True)

class MedicalSubQutionnaire(models.Model):
    _name = 'sub.questionnaire'
    _rec_name = 'question'

    product = fields.Many2one('insurance.product', 'Product', index=True)
    question = fields.Many2one('questionnaire.line.setup', domain="[('product_id', '=', product), ('question_type', '=', 'choose')]")
    questionnaire_ids = fields.One2many('questionnaire.line.setup', 'sub_questionnaire_id')
