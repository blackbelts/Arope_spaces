from odoo import models, fields, api
from datetime import timedelta, datetime

from dateutil.relativedelta import relativedelta

MONTHS = {1: 'Jan',
          2: 'Feb',
          3: 'Mar',
          4: 'Apr',
          5: 'May',
          6: 'Jun',
          7: 'Jul',
          8: 'Aug',
          9: 'Sep',
          10: 'Oct',
          11: 'Nov',
          12: 'Dec'}


class CRMTeam(models.Model):
    _inherit = 'crm.team'

    targets_id = fields.One2many(comodel_name="team.target", inverse_name="channel_id", string="Targets",
                                 required=False, )
    target_policy_ids = fields.One2many('target.policy','team_id',string='Target Policy')
    chain = fields.Many2many(comodel_name="res.users", string='Managers')



#
#
#
class TeamTarget(models.Model):
    _name = 'team.target'

    member = fields.Many2one(comodel_name="res.users", string="Member", required=False, )
    channel_id = fields.Many2one(comodel_name="crm.team", ondelete='cascade')
    type = fields.Selection(
        [("individual", "Individual"), ("corporate", "Corporate")],
        string="Type", default='individual', copy=True)
    is_new = fields.Boolean('Is New Partner',default=False)
    rate = fields.Float('Rate')
    targets = fields.One2many('target.rules', 'target_id', string='Target Lines')
    target_start = fields.Date(string='Start')
    Total_amount = fields.Float(string='Total Amount')
    no_months = fields.Integer('No Months')

    def create_target(self):
        date_start = self.target_start
        for i in range(self.no_months):
            date1 = datetime.strptime(str(date_start), '%Y-%m-%d').date()
            date3 = date1 + relativedelta(months=1)
            if self.is_new == True:
                self.targets = [(0, 0, {'name': MONTHS[datetime.strptime(str(date_start), '%Y-%m-%d').month],
                                        'from_date': date_start, 'to_date': date3 - relativedelta(days=1)
                    , 'amount': round(self.Total_amount / self.no_months,2) , 'member_id': self.member.id, 'target_id': self.id})]
            else:
                last_total = 0
                for pol in self.env['policy.arope'].search(
                        [('agent_code', '=', self.member.agent_code), ('issue_date', '>=', date_start - relativedelta(years=1)),
                         ('issue_date', '<', date_start + relativedelta(months=1))]):
                    last_total += pol.eq_total
                self.targets = [(0, 0, {'name': MONTHS[datetime.strptime(str(date_start), '%Y-%m-%d').month],
                                        'from_date': date_start, 'to_date': date3 - relativedelta(days=1)
                    , 'amount': round((self.rate * last_total)+ last_total, 2), 'member_id': self.member.id,
                                        'target_id': self.id})]
            date_start = date3
        self.calc_total_amount()

    @api.onchange('member')
    def set_member(self):
            return {'domain': {'member': [('id', 'in', self.channel_id.member_ids.ids)]}}


    def calc_total_amount(self):
        targets = []
        self.Total_amount = 0
        for rec in self.targets:
            self.Total_amount += rec.amount
            targets.append(rec)
        self.no_months = len(targets)


#
class TargetRules(models.Model):
    _name = 'target.rules'

    name = fields.Char()
    from_date = fields.Date('Date From')
    to_date = fields.Date('Date To')
    amount = fields.Float('Target')
    total_sales = fields.Float(string='Total Sales')
    target_percent = fields.Float('Percentage(%)')
    target_id = fields.Many2one('team.target', ondelete='cascade')
    member_id = fields.Many2one("res.users")
#
#
class TargetPolicy(models.Model):
    _name = 'target.policy'

    from_date = fields.Date('Date From')
    to_date = fields.Date('Date To')
    amount = fields.Float('Percentage(%)')
    line_of_business = fields.Many2many('insurance.line.business', string='Line of business')
    team_id = fields.Many2one('crm.team', ondelete='cascade')