from odoo import models, tools, fields, api

# class QuestionnaireSetup(models.Model):
#     _name = 'questionnaire.setup'
#     _rec_name = 'lob'
#     _description = 'Set up questionnaire'
#     lob = fields.Char('Line OF Business')
#     questions_ids = fields.One2many('questionnaire.line.setup', 'questionnaire_id')

class QuestionnaireLineSetup(models.Model):
    _name = 'questionnaire.line.setup'
    _rec_name= 'question'
    question = fields.Char('Question')
    # questionnaire = fields.Many2many('insurance.product', string="Related Questions")
    options = fields.Many2many('selection.options', sting="Selections")
    desc = fields.Char('Description')
    question_type = fields.Selection([('text', 'Text'), ('numerical', 'Numerical'), ('choose', 'Choose')],
                                     'Question Type', default='text')
    # question_type = fields.Selection([('text', 'Text'), ('numerical', 'Numerical'), ('boolean', 'True OR False')],
    #                                  'Question Type', default='text')
    # text = fields.Char('Text')
    # file = fields.Binary('File')
    # value = fields.Float('Value')
    # boolean_field = fields.Boolean('True Or False Answer', default=False)

    # selection_name = fields.Many2one('selections.setup', 'Selection Name', ondelele='cascade')
    # selection_field = fields.Many2one('selections.fields', 'Answer', ondelele='cascade', )
    # questionnaire_id = fields.Many2one('questionnaire.setup', ondelele='cascade', index=True)
    product_id = fields.Many2one('insurance.product', ondelele='cascade', index=True)

    # @api.onchange('selection_name')
    # def _get_selection(self):
    #     selections_list = self.env['selections.setup'].get_selection_field()
    #     return selections_list
    # @api.onchange('selection_name')
    # def get_selection_field(self):
    #     if self.selection_name:
    #         domain = [('selection_id', '=', self.selection_name)]
    #     else:
    #         domain = [('selection_id', 'in', [])]
    #
    #     return {'domain': {'selection_field': domain}}
    # @api.depends('selection_name')
    # def return_selection_field(self):
    #     # selection =
    #     selection_list = []
    #     for data in self.env['selections.setup'].search([('name', '=', self.selection_name.name)]).fields_ids:
    #         selection_list.append((data.value, data.name))
    #     print(selection_list)
    #     return selection_list
#
# class Selections(models.Model):
#     _name = 'selections.setup'
#     _rec = 'name'
#
#     name = fields.Char(string='Name', required=True)
#     usage = fields.Char(string='Description')
#     # in_use = fields.Boolean(string='Active', default=True)
#
#     fields_ids = fields.One2many('selections.fields', 'selection_id')
#
#
#
# class SelectionsFields(models.Model):
#     _name = 'selections.fields'
#     # _order = 'value asc'
#     _rec = 'name'
#
#     name = fields.Char(string='Option', required=True)
#     value = fields.Char(string='Value', required=True)
#     # in_use = fields.Boolean(string='Active', default=True)
#
#     selection_id = fields.Many2one('selections.setup', ondelele='cascade', index=True)
class SurveyLineSetup(models.Model):
    _name = 'survey.line.setup'
    _rec_name = 'question'
    question = fields.Char('Question')
    options = fields.Many2many('selection.options', sting="Selections")

    desc = fields.Char('Description')
    # question_type = fields.Selection([('text', 'Text'), ('numerical', 'Numerical'), ('choose', 'Choose')],
    #                                  'Question Type', default='text')
    # text = fields.Char('Text')
    # file = fields.Binary('File')
    # value = fields.Float('Value')
    # boolean_field = fields.Boolean('True Or False Answer', default=False)

    # selection_name = fields.Many2one('selections.setup', 'Selection Name', ondelele='cascade')
    # selection_field = fields.Many2one('selections.fields', 'Answer', ondelele='cascade', )
    # questionnaire_id = fields.Many2one('questionnaire.setup', ondelele='cascade', index=True)
    product_id = fields.Many2one('insurance.product', ondelele='cascade', index=True)

class FinalApplicationSetup(models.Model):
    _name = 'final.application.setup'
    _rec_name = 'description'
    description = fields.Char('Document Name')
    # application_files = fields.Binary('File')
    product_id = fields.Many2one('insurance.product', ondelele='cascade', index=True)

class OfferSetup(models.Model):
    _name = 'offer.setup'
    _rec_name = 'offer'
    offer = fields.Char('Offer Item')
    # application_files = fields.Binary('File')
    product_id = fields.Many2one('insurance.product', ondelele='cascade', index=True)