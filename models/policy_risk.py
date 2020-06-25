import base64
import logging
import math
from datetime import timedelta
from datetime import datetime
from xlrd import open_workbook

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class policyrisks(models.Model):
    _name = "policy.risk"
    _rec_name = 'risk_description'

    # def get_policy(self, cr, uid, view_id=None, view_type='form',
    #                     context=None, toolbar=False, submenu=False):
    #     if context is None:
    #         context = {}
    #     res = super(policyrisks, self).fields_view_get(cr, uid, view_id=view_id, view_type=view_type,
    #                                                          context=context, toolbar=toolbar, submenu=False)
    #     return res

    # @api.multi
    # def get_policy(self):
    #     print("skdjsjhfjkdshkhjdj5555555555555")
    #     return {
    #         'name': ('get policy'),
    #         'view_type': 'form',
    #         'view_mode': 'form',
    #         'res_model': 'policy.broker',
    #         'view_id': [(self.env.ref('smart_policy.policy_form_view').id), 'form'],
    #         'type': 'ir.actions.act_window',
    #         'target': 'current',
    #         # 'domain': [('id', '=', self.policy_risk_id.id)],
    #         'res_id': self.policy_risk_id.id,
    #
    #     }

    # @api.multi
    # def set_claim(self):
    #     print("skdjsjhfjkdshkhjdj5555555555555")
    #     return {
    #         'name': ('get policy'),
    #         'view_type': 'form',
    #         'view_mode': 'form',
    #         'res_model': 'policy.broker',
    #         'view_id': [(self.env.ref('smart_policy.policy_form_view').id), 'form'],
    #         'type': 'ir.actions.act_window',
    #         'target': 'current',
    #         # 'domain': [('id', '=', self.policy_risk_id.id)],
    #         'res_id': self.policy_risk_id.id,
    #
    #     }

    # @api.multi
    # def create_claim(self):
    #     tree = self.env.ref('smart_claim.tree_insurance_claim')
    #     form = self.env.ref('smart_claim.form_insurance_claim')
    #     return {
    #         'name': ('Claim'),
    #         'view_type': 'form',
    #         'view_mode': 'tree, form',
    #         'res_model': 'insurance.claim',
    #         # 'view_id': [(self.env.ref('smart_claim.tree_insurance_claim').id), 'tree'],
    #         'views': [(tree.id, 'tree'),
    #                   (form.id, 'form')],
    #         'type': 'ir.actions.act_window',
    #         'target': 'current',
    #
    #         'context': {'default_policy_number': self.policy_risk_id.id,
    #                     'default_lob': self.policy_risk_id.line_of_bussines.id, 'default_chassis_no': self.chassis_no,
    #                     'default_maker': self.Man.id,'default_model': self.model.id,'default_plate_no': self.plate_no,
    #                     'default_engine': self.engine,
    #                     'create': True},
    #         'domain': [('policy_number', '=', self.policy_risk_id.id)]
    #
    #     }

    # @api.one
    @api.depends('policy_risk_id')
    def _compute_risk_descriptionn(self):
        if self.policy_risk_id:
            if self.test == "person":
                self.risk_description = (str(self.job) if self.job else " " + "_") + "   " + (
                    str(self.name) + " - " if self.name else " " + "_") + "   " + (
                                            str(self.DOB) + " - " if self.DOB else " " + "_") + "   " + "   " + (
                                            str(self.family_member) if self.family_member else " " + "_")+ "   " + (
                    str(self.note) + " - " if self.note else " " + "_")

            if self.test == "vehicle":
                self.risk_description = (str(
                    self.car_tybe) + ' - ' if self.car_tybe else " " + "_") + "   " + (
                                            str(
                                                self.Man) + " - " if self.Man else " " + "_") + "  " + (
                                            str(
                                                self.model) + " - " if self.model else " " + "_") + "   " + (
                                            str(
                                                self.country_id) + " - " if self.country_id else " " + "_") + "   " + (
                                            str(
                                                self.year_of_made) + " - " if self.year_of_made else " " + "_") + "  " + "VCC: " + (
                                            str(self.motor_cc) if self.motor_cc else " " + "_") + "  " + "PN: " + (
                                            str(
                                                self.plate_no) + ' - ' if self.plate_no else " " + "_") + "  " + "CH: " + (
                                            str(
                                                self.chassis_no) + ' - ' if self.chassis_no else " " + "_") + "  " + "EN: " + (
                                            str(
                                                self.engine) + ' - ' if self.engine else " " + "_") + "   " + (
                                            str(
                                                self.license_expire_date) + " - " if self.license_expire_date else " " + "_") + "   " + "Type: " + (
                                            str(
                                                self.state_type) + " - " if self.state_type else " " + "_")

            if self.test == "cargo":
                self.risk_description = (str(
                    self.cargo_type) + " - " if self.cargo_type else " " + "_") + "  " + "FRM: " + (
                                            str(self.From) + " - " if self.From else " " + "_") + "   " + "TO: " + (
                                            str(self.To) + " - " if self.To else " " + "_")
            if self.test == "location":
                self.risk_description = (
                                            str(
                                                self.type) if self.type else " " + "_") + "  " + "ADD: " + (
                                            str(self.address) + " - " if self.address else " " + "_")

            if self.test == 'Group':
                self.risk_description = (str(
                    self.group_category) + " - " if self.group_category else " " + "_") + "   " + (
                                            str(self.group_count) + " - " if self.group_count else " " + "_") + (
                                            str(
                                                self.policy_risk_id.line_of_bussines.object) + " - " if self.policy_risk_id.line_of_bussines.object else " " + "_") + "   " +(
                                            str(
                                                self.cover_codes) + " - " if self.cover_codes else " ")
            if self.test == 'Project':
                self.risk_description = (str(
                    self.proj_name) + " - " if self.proj_name else " " + "_") + "   " + (
                                            str(self.machine_id) + " - " if self.machine_id else " " + "_")
        else:
            self.risk_description = "something is wrong"

    # premium
    sum_insured = fields.Float(string='Sum Insured')

    limitone = fields.Char('Limit in One')
    limittotal = fields.Char('Limit in Total')

    old_id = fields.Integer()
    old_id_end = fields.Integer()
    policy_risk_id = fields.Many2one("policy.arope", copy=True)

    test = fields.Char(related="policy_risk_id.check_item")
    # get_type = fields.Char(related="policy_risk_id.type_char")
    risk_description = fields.Char("Risk Description", compute="_compute_risk_descriptionn", store=True)
    # insured_object_type = fields.Char(compute='_compute_insured')
    customer = fields.Many2one(related='policy_risk_id.customer')
    broker = fields.Many2one(related='policy_risk_id.broker')
    # product_policy = fields.Many2one('insurance.product', compute='get_policy_info')
    # is_renewal = fields.Boolean(compute='get_policy_info')
    # endorsement_no = fields.Char(compute='get_policy_info')
    # total_sum_insured = fields.Float(compute='get_policy_info')
    # start_date = fields.Date(compute='get_policy_info')
    # end_date = fields.Date(compute='get_policy_info')
    # gross_perimum = fields.Float(compute='get_policy_info')
    # policy_status = fields.Text(compute='get_policy_info')
    # source_of_business = fields.Many2one('res.partner', compute='get_policy_info')
    # issuing = fields.Boolean(compute='get_policy_info', store=True)
    # si_deff = fields.Float('SI +/-')
    # active = fields.Boolean(string="Active", compute='get_policy_info')
    # line_of_bussines = fields.Many2one('insurance.line.business', compute='get_policy_info')
    # phone_number = fields.Char(compute='get_policy_info')
    # t_permimum = fields.Float(string="Net Premium", compute='get_policy_info')

    # @api.one
    # def get_policy_info(self):
    #     x = self.env["policy.broker"].search(
    #         ['|', ('active', '=', True), ('active', '=', False), ('id', '=', self.policy_risk_id.id)])
    #     self.customer = x.customer.id
    #     self.discount_party = x.discount_party.id
    #     self.company = x.company.id
    #     self.product_policy = x.product_policy.id
    #     self.is_renewal = x.is_renewal
    #     self.endorsement_no = x.endorsement_no
    #     self.total_sum_insured = x.total_sum_insured
    #     self.start_date = x.start_date
    #     self.end_date = x.end_date
    #     self.gross_perimum = x.gross_perimum
    #     self.policy_status = x.policy_status
    #     self.source_of_business = x.source_of_business.id
    #     self.issuing = x.issuing
    #     self.active = x.active
    #     self.phone_number = x.phone_number
    #     self.t_permimum = x.t_permimum



    # vechile_risk
    car_tybe = fields.Char( string='Vehicle Type',)
    Man = fields.Char(string='Maker',)
    model = fields.Char( string='Model',)
    state_type = fields.Selection([('new', 'New'),
                                   ('used', 'Used')],
                                  string='Type', track_visibility='onchange')
    year_of_made = fields.Char("Year of Make")
    country_id = fields.Many2one(string='Region')
    motor_cc = fields.Char("Motor cc")
    chassis_no = fields.Char("Chassis Number")
    plate_no = fields.Char("Plate Number")
    engine = fields.Char("Engine Number")
    add_info = fields.Text("Additional Info")
    license_expire_date = fields.Date('License Expiration Date')
    # person_risk
    name = fields.Char('Name', copy=True)
    note = fields.Char('Note', copy=True)
    DOB = fields.Date('Date Of Birth', copy=True)
    job = fields.Many2one( string='Job Type')
    family_member = fields.Selection([('principle', 'Principle'),
                                      ('spouse', 'Spouse'),
                                      ('kid', 'Kid'), ],
                                     'Family Member', track_visibility='onchange')

    # cargo_risk
    cargo_type = fields.Many2one(string='Type of Goods')
    From = fields.Char('From')
    To = fields.Char('To')

    # location
    type = fields.Many2one(string='Location Type')
    address = fields.Char('Address')
    risk_details = fields.Text('Risk Details')
    # group group
    group_category = fields.Char('Category')
    cover_codes = fields.Char('Covers')
    group_count = fields.Integer('Count')
    # group_premium=fields.Float('')
    group_premium = fields.Float(string="", required=False, )
    # rate = fields.Float(related='policy_risk_id.rate')
    # project_risk
    proj_name = fields.Char('Project Name')
    proj_start_date = fields.Date('Start Date')
    proj_end_date = fields.Date('End Date')
    proj_description = fields.Text('Project Description')
    machine_id = fields.Char('Machine ID')
    # risk_groups_ids = fields.One2many('risk.groups', 'risk_id', string='Group Members')

    _sql_constraints = [
        ('risk_unique', 'unique(policy_risk_id,risk_description)', 'ID already exists!')]


# class RiskGroup(models.Model):
#     _name = "risk.groups"
#     _rec_name = 'member_id'
#
#     name = fields.Char('Name')
#     dob = fields.Date(string="Date Of Birth", required=False, )
#     member_id = fields.Char('Member ID')
#     customer = fields.Many2one('res.partner', related='policy_id.customer', store=True)
#     member_type = fields.Selection(related='risk_id.policy_risk_id.line_of_bussines.object')
#     card_num = fields.Char(string="Card Number", required=False, )
#     employee_code_mic = fields.Text('Employee Code MIC')
#     status = fields.Char('Status')
#     relation = fields.Char('Relation')
#     gender = fields.Char(string="Gender", required=False, )
#     risk_id = fields.Many2one('policy.risk')
#     policy_id = fields.Many2one("policy.broker")
#     policy_active = fields.Boolean(related='policy_id.active',store=True)
#     crm_id = fields.Many2one("crm.lead")
#     group_name = fields.Char("Benefit Name")
#     is_current = fields.Boolean(string="Active",compute='_compute_is_current')
#     start_date = fields.Date(string="Start Date")
#     end_date = fields.Date(string="End Date")
#     head_family_name = fields.Char(string="Head Of Family Name", required=False, )
#     head_family_id = fields.Char(string="Head Family ID", required=False, )
#     sum_insured = fields.Float(string="", required=False)
#
#     @api.multi
#     @api.depends('end_date')
#     def _compute_is_current(self):
#         for rec in self:
#             if rec.end_date:
#                 today = datetime.today().date()
#                 end_date = datetime.strptime(rec.end_date, '%Y-%m-%d').date()
#                 if end_date >= today:
#                     rec.is_current = True
#
#
# class NewModulecleanrisk(models.Model):
#     _name = 'data.clean.setup.risk'
#
#     clean_option_maker = fields.Boolean('Clean Maker')
#     clean_option_model = fields.Boolean('Clean Model')
#
#     maker = fields.Many2one('insurance.setup', string='Maker', domain="[('setup_key','=','man')]")
#     model = fields.Many2one('insurance.setup', string='Model', domain="[('setup_key','=','model')]")
#
#     @api.multi
#     def replace_setup_risk(self):
#         context = dict(self._context or {})
#         active_ids = context.get('active_ids', []) or []
#         if self.clean_option_model:
#             for rec in self.env['policy.risk'].browse(active_ids):
#                 print(5555555555)
#                 if self.model:
#                     rec.write({'model': self.model.id})
#                     rec._compute_risk_descriptionn()
