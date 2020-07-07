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

ROUNDING_FACTOR = 16

from odoo import models, fields, api, exceptions
class Brokers(models.Model):
    _name = 'arope.broker'
    @api.model
    def get_production(self, id):
        total = 0
        ids=[]
        for prod in self.env['policy.arope'].search([('broker.id', '=', id)]):
            total += prod.gross_premium
            ids.append(prod.id)
        return {"total":total,"ids":ids}

    def get_all_production(self):
        prod = {}
        for user in self.env['res.users'].search([('partner_id.broker', '=', True)]):
            total = 0.0
            for pro in self.env['policy.arope'].search([('broker.id', '=', user.id)]):
                total += pro.gross_premium
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
            return list(result.keys()).index(id)
        # if id in result.items():
        #    return
        else:
            raise exceptions.ValidationError('Broker no Production')

    @api.model
    def get_target_production(self, id):
        result = {}
        targetlist = []
        production = []
        result1 = {}
        finalTarget = []
        finalProduction = []
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        for target in self.env['team.target'].search([('member.id', '=', id)]):
            for rule in target.targets:
                total = 0.0
                for pol in self.env['policy.arope'].search(
                        [('broker.id', '=', id), ('start_date', '>=', rule.from_date),
                         ('start_date', '<=', rule.to_date)]):
                    total += pol.gross_premium
                result[rule.name] = [rule.amount, total]
        del result[False]
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
    def get_production_compare(self, id):
        date_last_year = date(date.today().year, 1, 1) - relativedelta(years=1)
        date_start = date(date.today().year, 1, 1)
        date3 = date_start
        current_total = 0.0
        current_prod = []
        last_total = 0.0
        last_prod = []
        for i in range(12):
            for pol in self.env['policy.arope'].search(
                    [('broker.id', '=', id), ('start_date', '>=', date3),
                     ('start_date', '<', date3 + relativedelta(months=1))]):
                current_total += pol.gross_premium
            current_prod.append(current_total)
            for pol in self.env['policy.arope'].search(
                    [('broker.id', '=', id), ('start_date', '>=', date_last_year),
                     ('start_date', '<', date_last_year + relativedelta(months=1))]):
                last_total += pol.gross_premium
            last_prod.append(last_total)

            date3 = date3 + relativedelta(months=1)
            date_last_year = date_last_year + relativedelta(months=1)
        return {'current_year': current_prod, 'last_year': last_prod}

    @api.model
    def get_renew(self, id):
        result={}
        ids = []
        
        for rec in self.env['system.notify'].search([('type','=','Renewal')]):
            if rec.color=='Green':
                ids=[]
                date1=datetime.today().date()+relativedelta(days=rec.no_days)
                total = 0
                for prod in self.env['policy.arope'].search([('broker.id', '=', id),('end_date', '>=', datetime.today().date()),('end_date', '<=', date1),]):
                    total += prod.gross_premium
                    ids.append(prod.id)
                result[rec.color]={'total':total,'count':len(ids),'ids':ids}
            
            elif rec.color=='Orange':
                ids=[]
                #rec.no_days*=-1
                date1 = datetime.today().date() - relativedelta(days=rec.no_days)
                total = 0
                for prod in self.env['policy.arope'].search([('broker.id', '=', id), ('end_date', '<=', datetime.today().date()),('end_date', '>=', date1)]):
                    total += prod.gross_premium
                    ids.append(prod.id)
                result[rec.color]={'total':total,'count':len(ids),'ids':ids}

            else:
                ids=[]
                date1 = datetime.today().date() - relativedelta(days=rec.no_days)
                total = 0
                for prod in self.env['policy.arope'].search(
                        [('broker.id', '=', id), ('end_date', '<=', datetime.today().date() - relativedelta(days=self.env['system.notify'].search([('type','=','Renewal'),('color','=','Orange')],limit=1).no_days)),
                         ]):
                    total += prod.gross_premium
                    ids.append(prod.id)

                result[rec.color]={'total':total,'count':len(ids),'ids':ids}
        return result

    @api.model
    def get_collections(self, id):
        result = {}
        ids = []
        colors=[]
        for rec in self.env['system.notify'].search([('type', '=', 'Collection')]):
            if rec.color == 'Green':
                ids = []
                date1=datetime.today().date()+relativedelta(days=rec.no_days)
                total = 0
                for prod in self.env['collection.arope'].search([('broker.id', '=', id), ('state', '=', 'outstanding'),('collect_date', '>=', datetime.today().date()),('collect_date', '<=', date1) ]):
                    total += prod.gross_premium
                    ids.append(prod.id)
                result[rec.color] = {'total':total,'count':len(ids),'ids':ids}
                
            elif rec.color=='Orange':
                ids = []
                #rec.no_days*=-1
                date1 = datetime.today().date() - relativedelta(days=rec.no_days)
                total = 0
                for prod in self.env['collection.arope'].search([('broker.id', '=', id), ('state', '=', 'outstanding'), ('collect_date', '<=', datetime.today().date()),('collect_date', '>=', date1)]):
                    total += prod.gross_premium
                    ids.append(prod.id)
                result[rec.color] = {'total':total,'count':len(ids),'ids':ids}

            else:
                ids = []
                date1 = datetime.today().date() - relativedelta(days=rec.no_days)
                total = 0
                for prod in self.env['collection.arope'].search([('broker.id', '=', id), ('state', '=', 'outstanding'),('collect_date', '<=', datetime.today().date() - relativedelta(days=self.env['system.notify'].search([('type','=','Collection'),('color','=','Orange')],limit=1).no_days)), ]):
                # for prod in self.env['collection.arope'].search([('broker.id', '=', id),('state', '=', 'outstanding'), ('collect_date', '<=', date.today() - relativedelta(days=self.env['collection.arope'].search([('type','=','Collection'),('color','=','Orange')])))]):
                # self.env['collection.arope'].search([('broker.id', '=', id),('state', '=', 'outstanding'), ('collect_date', '<=', datetime.today().date() - relativedelta(days=self.env['collection.arope'].search([('type','=','collect_date'),('color','=','Orange')]), ]):
                    total += prod.policy.gross_premium
                    ids.append(prod.id)
                result[rec.color] = result[rec.color] = {'total':total,'count':len(ids),'ids':ids}
        return result

    @api.model
    def get_dashboard(self, id):

        return {
            "production": self.get_production(id),
            'rank': self.get_rank(id),
            'targetVsProduction': self.get_target_production(id),
            'lastVsCurrentYear': self.get_production_compare(id),

        }