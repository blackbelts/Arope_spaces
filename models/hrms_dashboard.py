# -*- coding: utf-8 -*-
from collections import defaultdict
from datetime import timedelta, datetime, date
from dateutil.relativedelta import relativedelta
import pandas as pd
from pytz import utc
from odoo import models, fields, api, _
from odoo.http import request
from collections import OrderedDict
from odoo.tools import float_utils
import base64


ROUNDING_FACTOR = 16

from odoo import models, fields, api, exceptions
class Brokers(models.Model):
    _name = 'arope.broker'

    @api.model
    def get_production(self,agents_codes):
        total = 0.0
        ids=[]
        for prod in self.env['policy.arope'].search([('agent_code', 'in', agents_codes)]):
            total += prod.totoal_premium
            ids.append(prod.id)
        return {"total":total,"ids":ids}

    def get_all_production(self):
        prod = {}
        for user in self.env['res.users'].search([('is_broker','=',True)]):
            total = 0.0
            agents_codes = []
            for rec in self.env['persons'].search([('card_id', '=', user.card_id)]):
                agents_codes.append(rec.agent_code)
            for pro in self.env['policy.arope'].search([('agent_code', 'in', agents_codes)]):
                total += pro.totoal_premium
            prod[user.id] = total
        print(prod)
        print('''''''''''''''''''''''''''''''''''')
        print({k: v for k, v in sorted(prod.items(), key=lambda item: item[1])})
        return {k: v for k, v in sorted(prod.items(), key=lambda item: item[1], reverse=True)}

    @api.model
    def get_rank(self, id):
        print('''''''''''''''''''''''''''''''''''')
        print(id)
        result = self.get_all_production()
        if id in list(result.keys()):
            return (list(result.keys()).index(id))+1
        # if id in result.items():
        #    return
        # else:
        #     raise exceptions.ValidationError('Broker no Production')

    @api.model
    def get_target_production(self, id):
        result = {}
        targetlist = []
        production = []
        result1 = {}
        finalTarget = []
        finalProduction = []
        agents_codes = []
        card = self.env['res.users'].search([('id', '=', id)], limit=1).card_id
        for rec in self.env['persons'].search([('card_id', '=', card)]):
            agents_codes.append(rec.agent_code)
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        for target in self.env['team.target'].search([('member.id', '=', id)]):
            for rule in target.targets:
                total = 0.0
                for pol in self.env['policy.arope'].search(
                        [('agent_code', 'in', agents_codes), ('issue_date', '>=', rule.from_date),
                         ('issue_date', '<=', rule.to_date)]):
                    total += pol.totoal_premium
                result[rule.name] = [rule.amount, total]
        #del result[False]
        x = OrderedDict(sorted(result.items(), key=lambda x: months.index(x[0])))
        for key, value in x.items():
            targetlist.append(value[0])
            production.append(value[1])
        targetNum = 0
        productionNum = 0
        for rec in targetlist:
            targetNum += rec
            finalTarget.append(targetNum)
        for record in production:
            productionNum += record
            finalProduction.append(productionNum)
        result1 = {'target': finalTarget, 'production': finalProduction}
        return result1

    @api.model
    def get_production_compare(self, agents_codes):
        date_last_year = date(date.today().year, 1, 1) - relativedelta(years=1)
        date_start = date(date.today().year, 1, 1)
        date3 = date_start
        current_total = 0.0
        current_prod = []
        last_total = 0.0
        last_prod = []

        for i in range(12):
            for pol in self.env['policy.arope'].search(
                    [('agent_code', 'in', agents_codes), ('issue_date', '>=', date3),
                     ('issue_date', '<', date3 + relativedelta(months=1))]):
                current_total += pol.totoal_premium
            current_prod.append(current_total)
            for pol in self.env['policy.arope'].search(
                    [('agent_code', 'in', agents_codes), ('issue_date', '>=', date_last_year),
                     ('issue_date', '<', date_last_year + relativedelta(months=1))]):
                last_total += pol.totoal_premium
            last_prod.append(last_total)

            date3 = date3 + relativedelta(months=1)
            date_last_year = date_last_year + relativedelta(months=1)
        return {'current_year': current_prod, 'last_year': last_prod}

    @api.model
    def get_renew(self, agents_codes):
        result={}
        ids = []
        for rec in self.env['system.notify'].search([('type','=','Renewal')]):
            if rec.color=='Green':
                ids=[]
                date1=datetime.today().date()+relativedelta(days=rec.no_days)
                total = 0
                for prod in self.env['policy.arope'].search([('agent_code', 'in', agents_codes),('expiry_date', '>=', datetime.today().date()),('expiry_date', '<=', date1),]):
                    total += prod.totoal_premium
                    ids.append(prod.id)
                result[rec.color]={'total':total,'count':len(ids),'ids':ids}

            elif rec.color=='Orange':
                ids=[]
                #rec.no_days*=-1
                date1 = datetime.today().date() - relativedelta(days=rec.no_days)
                total = 0
                for prod in self.env['policy.arope'].search([('agent_code', 'in',agents_codes), ('expiry_date', '<=', datetime.today().date()),('expiry_date', '>=', date1)]):
                    total += prod.totoal_premium
                    ids.append(prod.id)
                result[rec.color]={'total':total,'count':len(ids),'ids':ids}

            else:
                ids=[]
                date1 = datetime.today().date() - relativedelta(days=rec.no_days)
                total = 0
                for prod in self.env['policy.arope'].search(
                        [('agent_code', 'in', agents_codes), ('expiry_date', '<=', datetime.today().date() - relativedelta(days=self.env['system.notify'].search([('type','=','Renewal'),('color','=','Orange')],limit=1).no_days)),
                         ]):
                    total += prod.totoal_premium
                    ids.append(prod.id)

                result[rec.color]={'total':total,'count':len(ids),'ids':ids}
        return result

    @api.model
    def get_collections(self, agents_codes):
        result = {}
        ids = []
        colors=[]
        for rec in self.env['system.notify'].search([('type', '=', 'Collection')]):
            if rec.color == 'Green':
                ids = []
                date1=datetime.today().date()+relativedelta(days=rec.no_days)
                total = 0
                for prod in self.env['collection.arope'].search([('agent_code', 'in', agents_codes),('prem_date', '>=', datetime.today().date()),('prem_date', '<=', date1) ]):
                    total += prod.total_lc
                    ids.append(prod.id)
                result[rec.color] = {'total':total,'count':len(ids),'ids':ids}
            elif rec.color=='Orange':
                ids = []
                #rec.no_days*=-1
                date1 = datetime.today().date() - relativedelta(days=rec.no_days)
                total = 0
                for prod in self.env['collection.arope'].search([('agent_code', 'in',agents_codes ), ('prem_date', '<=', datetime.today().date()),('prem_date', '>=', date1)]):
                    total += prod.total_lc
                    ids.append(prod.id)
                result[rec.color] = {'total':total,'count':len(ids),'ids':ids}
            else:
                ids = []
                date1 = datetime.today().date() - relativedelta(days=rec.no_days)
                total = 0
                for prod in self.env['collection.arope'].search([('agent_code', 'in',agents_codes),('prem_date', '<=', datetime.today().date() - relativedelta(days=self.env['system.notify'].search([('type','=','Collection'),('color','=','Orange')],limit=1).no_days)), ]):
                # for prod in self.env['collection.arope'].search([('broker.id', '=', id),('state', '=', 'outstanding'), ('prem_date', '<=', date.today() - relativedelta(days=self.env['collection.arope'].search([('type','=','Collection'),('color','=','Orange')])))]):
                # self.env['collection.arope'].search([('broker.id', '=', id),('state', '=', 'outstanding'), ('prem_date', '<=', datetime.today().date() - relativedelta(days=self.env['collection.arope'].search([('type','=','prem_date'),('color','=','Orange')]), ]):
                    total += prod.policy.total_lc
                    ids.append(prod.id)
                result[rec.color] = result[rec.color] = {'total':total,'count':len(ids),'ids':ids}
        return result

    @api.model
    def get_lob_and_products(self):
        lob = []
        products = []
        quote = []
        for rec in self.env['insurance.line.business'].search([]):
            lob.append({'id':rec.id, 'name':rec.line_of_business})
        for product in self.env['insurance.product'].search([]):
            products.append({'id': product.id,'name':product.product_name, 'lob_id': product.line_of_bus.id})
        for rec in self.env['state.setup'].search([('status', '=', 'quick_quote'),('type', '=', 'insurance_app')]).product_ids:
            if rec.line_of_bus.line_of_business == 'Motor':
                for product in self.env['product.covers'].search([]):
                    quote.append({'name': product.product_name, 'id': product.id, 'lob_id': rec.line_of_bus.id})
            elif rec.line_of_bus.line_of_business == 'Medical':
                for product in self.env['medical.price'].search([]):
                    quote.append({'name': product.product_name, 'package': product.package, 'id': product.id, 'lob_id': rec.line_of_bus.id})

        return {'lob': lob, 'products': products, 'quote': quote}

    @api.model
    def upload_document(self, data):
        Model = request.env['ir.attachment']
        attachment = Model.create({
            'name': 'test',
            'datas_fname': 'test',
            'res_name': 'test',
            'type': 'binary',
            'datas': data,
        })
        return attachment.id

    @api.model
    def get_dashboard(self, id):
        card = self.env['res.users'].search([('id', '=', id)], limit=1).card_id
        agents_codes = []
        for rec in self.env['persons'].search([('card_id', '=', card)]):
            agents_codes.append(rec.agent_code)
        return {
            "production": self.get_production(agents_codes),
            'rank': self.get_rank(id),
            'targetVsProduction': self.get_target_production(id),
            'lastVsCurrentYear': self.get_production_compare(agents_codes),
            'collections':self.get_collections(agents_codes),
            'renews':self.get_renew(agents_codes)
        }

    @api.model
    def get_policy(self,id,limit,offset):
        card = self.env['res.users'].search([('id', '=', id)], limit=1).card_id
        agents_codes = []
        for rec in self.env['persons'].search([('card_id', '=', card)]):
            agents_codes.append(rec.agent_code)
        return {'policies':self.env['policy.arope'].search_read([('agent_code', 'in', agents_codes)],limit=limit,offset=offset),'count':self.env['policy.arope'].search_count([('agent_code', 'in', agents_codes)])}

    @api.model
    def get_claim(self, id,limit,offset):
        card = self.env['res.users'].search([('id', '=', id)], limit=1).card_id
        agents_codes = []
        for rec in self.env['persons'].search([('card_id', '=', card)]):
            agents_codes.append(rec.agent_code)
        return {'claims':self.env['claim.arope'].search_read([('agent_code', 'in', agents_codes)],limit=limit,offset=offset),'count':self.env['claim.arope'].search_count([('agent_code', 'in', agents_codes)])}
