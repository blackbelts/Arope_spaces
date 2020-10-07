# -*- coding: utf-8 -*-
from collections import defaultdict
from datetime import timedelta, datetime, date
from dateutil.relativedelta import relativedelta
import pandas as pd
from pytz import utc
from odoo import models, fields, api, _
from odoo.http import request
from collections import OrderedDict
from odoo import http
from odoo.http import request
from odoo.tools import float_utils
import base64
import requests



ROUNDING_FACTOR = 16

from odoo import models, fields, api, exceptions
class Brokers(models.Model):
    _name = 'arope.broker'

    @api.model
    def get_production(self,agents_codes,type):
        if type=='broker':
            domain=[('agent_code', 'in', agents_codes)]
        elif type=='customer':
            domain=[('customerpin', 'in', agents_codes)]
        else:
            domain=[]

        total = 0.0
        ids=[]
        for prod in self.env['policy.arope'].search(domain):
            total += prod.totoal_premium
            ids.append(prod.id)
        return {"total":total,"ids":ids}

    def get_all_production(self):
        prod = {}
        total = 0.0

        for user in self.env['persons'].search([('is_user','=',True), ('type', '=', 'broker')]):
           for pro in self.env['policy.arope'].search([('agent_code', '=', user.agent_code)]):
                total += pro.totoal_premium
           prod[user.related_user.id] = total
        print(prod)
        print('''''''''''''''''''''''''''''''''''')
        print({k: v for k, v in sorted(prod.items(), key=lambda item: item[1])})
        return {k: v for k, v in sorted(prod.items(), key=lambda item: item[1], reverse=True)}

    @api.model
    def get_rank(self,id):
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
                for prod in self.env['collection.arope'].search([('agent_code', 'in', agents_codes),('prem_date', '>=', datetime.today().date()),('due_date', '<=', date1) ]):
                    total += prod.total_lc
                    ids.append(prod.id)
                result[rec.color] = {'total':total,'count':len(ids),'ids':ids}
            elif rec.color=='Orange':
                ids = []
                #rec.no_days*=-1
                date1 = datetime.today().date() - relativedelta(days=rec.no_days)
                total = 0
                for prod in self.env['collection.arope'].search([('agent_code', 'in',agents_codes ), ('prem_date', '<=', datetime.today().date()),('due_date', '>=', date1)]):
                    total += prod.total_lc
                    ids.append(prod.id)
                result[rec.color] = {'total':total,'count':len(ids),'ids':ids}
            else:
                ids = []
                date1 = datetime.today().date() - relativedelta(days=rec.no_days)
                total = 0
                for prod in self.env['collection.arope'].search([('agent_code', 'in',agents_codes),('due_date', '<=', datetime.today().date() - relativedelta(days=self.env['system.notify'].search([('type','=','Collection'),('color','=','Orange')],limit=1).no_days)), ]):
                # for prod in self.env['collection.arope'].search([('broker.id', '=', id),('state', '=', 'outstanding'), ('prem_date', '<=', date.today() - relativedelta(days=self.env['collection.arope'].search([('type','=','Collection'),('color','=','Orange')])))]):
                # self.env['collection.arope'].search([('broker.id', '=', id),('state', '=', 'outstanding'), ('prem_date', '<=', datetime.today().date() - relativedelta(days=self.env['collection.arope'].search([('type','=','prem_date'),('color','=','Orange')]), ]):
                    total += prod.total_lc
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
    def upload_questionnaire(self, data):

        # attachment = request.env['ir.attachment'].sudo().create({
        #     'name': 'Questionnaire',
        #     # 'datas_fname': 'questionnaire',
        #     'res_name': 'questionnaire',
        #     'type': 'binary',
        #     'datas': data['file'],
        # })
        self.env['insurance.quotation'].search([('id', '=', data['id'])]).write({'upload_questionnaire':[(0,0,{'name': 'Questionnaire',
            # 'datas_fname': 'questionnaire',
            'res_name': 'questionnaire',
            'type': 'binary',
            'datas': data['file']})],'request_for_ofer_state': 'complete'})
        self.env['state.history'].create({"application_id": data['id'], "state": 'proposal', 'sub_state': 'complete',
                                          "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                          "user": self.env['insurance.quotation'].search(
                                              [('id', '=', data['id'])]).write_uid.id})
        return True

    @api.model
    def upload_documents(self,data):

        self.env['final.application'].search([('id', '=', data['file_id'])]).write({'application_files': [(0,0, {
            'name': 'File',
            'res_name': 'questionnaire',
            'type': 'binary',
            'datas': data['file'],
        })], 'issue_in_progress_state': 'complete'})
        # self.self.env['insurance.quotation'].search([('id', '=', data['id'])]).write({})
        self.env['state.history'].create({"application_id": data['id'], "state": 'offer', 'sub_state': 'complete',
                                          "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                          "user": self.env['insurance.quotation'].search(
                                              [('id', '=', data['id'])]).write_uid.id})

        return True

    @api.model
    def get_lob_count_policy(self, agents_codes):

        lob_list = []
        for lob in self.env['insurance.line.business'].search([]):
            count = self.env['policy.arope'].search_count([('agent_code', 'in', agents_codes), ('lob', '=', lob.line_of_business)])
            if count>0:
             lob_list.append({'name':lob.line_of_business,'count':count,'icon':lob.image})
            else:continue

        return lob_list

    @api.model
    def get_lob_count_claim(self, agents_codes):
        lob_list = []
        for lob in self.env['insurance.line.business'].search([]):
            count = self.env['claim.arope'].search_count([('agent_code', 'in', agents_codes), ('lob', '=', lob.line_of_business)])
            if count > 0:
                lob_list.append({'name': lob.line_of_business, 'count': count, 'icon': lob.image})
            else:
                continue
        return lob_list

    @api.model
    def get_complaint_count(self, agents_codes):
        complaint_list = []
        for stage in self.env['helpdesk_lite.stage'].search([]):
            count = self.env['helpdesk_lite.ticket'].search_count(
                [('agent_code', 'in', agents_codes), ('stage_id', '=', stage.id)])
            complaint_list.append({'stage':stage.name,'count':count})
        return complaint_list

    @api.model
    def get_collection_ratio(self, agents_codes):
        complaint_list = []
        collections=0.0
        for coll in self.env['collection.arope'].search([('agent_code', 'in', agents_codes)]):
          collections+=coll.paid_lc
        prod=self.get_production(agents_codes)['total']
        if prod>0:
            ratio=(collections/prod)
            return  ratio
        else:
            return 0.0

    @api.model
    def get_claim_ratio(self, agents_codes):
        claims = 0.0
        for claim in self.env['claim.arope'].search([('agent_code', 'in', agents_codes)]):
            claims += claim.claim_paid
        prod = self.get_production(agents_codes)['total']
        if prod > 0:
            ratio = (claims / prod)
            return ratio
        else:
            return 0.0

    @api.model
    def get_dashboard(self, id):
        user = self.env['res.users'].search([('id', '=', id)], limit=1)
        agents_codes = []
        for rec in self.env['persons'].search([('card_id', '=', user.card_id)]):
            agents_codes.append(rec.agent_code)

        return {
            "user": self.env['persons'].search_read([('card_id', '=', user.card_id)],limit=1),
            "production": self.get_production(agents_codes,'broker'),
            "policy_lob": self.get_lob_count_policy(agents_codes),
            "claim_lob": self.get_lob_count_claim(agents_codes),
            "complaint_count": self.get_complaint_count(agents_codes),
            "collection_ratio": self.get_collection_ratio(agents_codes),
            "claims_ratio": self.get_claim_ratio(agents_codes),
            'rank': self.get_rank(id),
            'targetVsProduction': self.get_target_production(id),
            'lastVsCurrentYear': self.get_production_compare(agents_codes),
            'collections':self.get_collections(agents_codes),
            'renews':self.get_renew(agents_codes)
        }
    @api.model
    def get_user_groups(self,id):
        groups=[]
        for rec in self.env['res.groups'].sudo().search([('users','=',[id]),('category_id','=','arope')]):
            groups.append(rec.name)
        return groups
    # @api.model
    # def get_customer_dashboard(self, id):
    #     card = self.env['res.users'].search([('id', '=', id)], limit=1).card_id
    #     agents_codes = []
    #     for rec in self.env['persons'].search([('card_id', '=', card)]):
    #         agents_codes.append(rec.pin)
    #     return {
    #         "production": self.get_production(agents_codes,'customer'),
            # "policy_lob": self.get_lob_count_policy(agents_codes),
            # "claim_lob": self.get_lob_count_claim(agents_codes),
            # "complaint_count": self.get_complaint_count(agents_codes),
            # "collection_ratio": self.get_collection_ratio(agents_codes),
            # "claims_ratio": self.get_claim_ratio(agents_codes),
            # 'rank': self.get_rank(id),
            # 'targetVsProduction': self.get_target_production(id),
            # 'lastVsCurrentYear': self.get_production_compare(agents_codes),
            # 'collections': self.get_collections(agents_codes),
            # 'renews': self.get_renew(agents_codes)
        # }

    @api.model
    def get_policy(self,parms):
        card = self.env['res.users'].search([('id', '=', parms['id'])], limit=1).card_id
        agents_codes = []
        for rec in self.env['persons'].search([('card_id', '=', card)]):
            agents_codes.append(rec.agent_code)
        if parms['policy_num']:
            domain=[('agent_code', 'in', agents_codes),('policy_num','ilike',parms['policy_num'])]
        else:
            domain=[('agent_code', 'in', agents_codes)]
        return {'policies':self.env['policy.arope'].search_read(domain,limit=parms['limit'],offset=parms['offset']),'count':self.env['policy.arope'].search_count(domain)}

    @api.model
    def get_claim(self, parms):
        card = self.env['res.users'].search([('id', '=', parms['id'])], limit=1).card_id
        agents_codes = []
        for rec in self.env['persons'].search([('card_id', '=', card)]):
            agents_codes.append(rec.agent_code)
        if parms['claim_no']:
                domain = [('agent_code', 'in', agents_codes), ('claimNo', 'ilike', parms['claim_no'])]
        else:
                domain = [('agent_code', 'in', agents_codes)]
        return {'claims':self.env['claim.arope'].search_read(domain,limit=parms['limit'],offset=parms['offset']),'count':self.env['claim.arope'].search_count(domain)}

    @api.model
    def get_unpaid(self, parms):
        card = self.env['res.users'].search([('id', '=', parms['id'])], limit=1).card_id
        agents_codes = []
        for rec in self.env['persons'].search([('card_id', '=', card)]):
            agents_codes.append(rec.agent_code)
        if parms['policy_num']:
            domain = [('agent_code', 'in', agents_codes), ('policy_no', 'ilike', parms['policy_num'])]
        else:
            domain = [('agent_code', 'in', agents_codes)]
        return {'unpaids': self.env['collection.arope'].search_read(domain, limit=parms['limit'], offset=parms['offset']),
                'count': self.env['collection.arope'].search_count(domain)}

    @api.model
    def create_insurance_app(self,data):
        # card = self.env['res.users'].search([('id', '=', data['user_id'])], limit=1).card_id
        states= []
        for rec in self.env['state.setup'].search([('product_ids', 'in', [data['product_id']]),
                                                   ('type', '=', 'insurance_app'),
                                                   ('state_for', '=', 'broker')]):
            states.append(rec.state)
        if 'Quick Quote' in states:
            if data['id'] == False:
                if self.env['insurance.line.business'].search([('id', '=', data['lob'])]).line_of_business == 'Motor':
                    id = self.env['insurance.quotation'].create({'lob': data['lob'], 'product_id': data['product_id'],
                                                                 'name': data['name'], 'phone': data['phone'],
                                                                 'email': data['email'],
                                                                 'test_state': self.env['state.setup'].search(
                                                                     [('state', '=', 'Quick Quote')]).id,'state': 'quick_quote', 'deductible': data['deductible'],
                                                                 'target_price': data['target_price'], 'brand': data['brand'], 'sum_insured': data['sum_insured']})


                    self.env['insurance.quotation'].search([('id', '=', id.id)]).calculate_motor_price()
                    self.env['insurance.quotation'].search([('id', '=', id.id)]).compute_application_number()
                    self.env['insurance.quotation'].search([('id', '=', id.id)]).get_questions()
                    record = self.env['insurance.quotation'].search_read([('id', '=', id.id)])
                    return {'steps': states, 'app': record}
                elif self.env['insurance.line.business'].search([('id', '=', data['lob'])]).line_of_business == 'Medical':
                    id = self.env['insurance.quotation'].create({'lob': data['lob'], 'product_id': data['product_id'],
                                                                 'name': data['name'], 'phone': data['phone'],
                                                                 'email': data['email'],
                                                                 'test_state': self.env['state.setup'].search(
                                                                     [('state', '=', 'Quick Quote')]).id,
                                                                 'state': 'quick_quote',
                                                                 'target_price': data['target_price'],
                                                                 'package': data['package'], 'product': data['product'],
                                                                 'dob': data['dob']
                                                                 })
                    if data['family_age']:
                        for rec in data['family_age']:
                            f = self.env['medical.family'].create(
                                {'name': rec['name'], 'DOB': rec['dob'],
                                 'type': rec['type'],
                                 'gender': rec['gender'], 'application_id': id.id})

                            self.env['medical.family'].search([('id', '=', f.id)]).get_age()
                    self.env['insurance.quotation'].search([('id', '=', id.id)]).calculate_price()
                    self.env['insurance.quotation'].search([('id', '=', id.id)]).compute_application_number()
                    self.env['insurance.quotation'].search([('id', '=', id.id)]).get_questions()
                    record = self.env['insurance.quotation'].search_read([('id', '=', id.id)])
                    return {'steps': states, 'app': record}


            else:

                id = self.env['insurance.quotation'].search([('id', '=', data['id'])])[0]
                id.write({'lob': data['lob'], 'product_id': data['product_id'],
                                                             'name': data['name'], 'phone': data['phone'],
                                                             'email': data['email'],'deductible': data['deductible'],
                                                             'test_state': self.env['state.setup'].search(
                                                                 [('state', '=', 'Quick Quote')]).id,'state': 'quick_quote',
                                                             'target_price': data['target_price'], 'brand': data['brand'],
                                                                'sum_insured': data['sum_insured'],'package': data['package'],
                                                                'product': data['product'],
                                                                 'dob': data['dob']})
                if self.env['insurance.quotation'].search([('id', '=', id.id)]).lob.line_of_business == 'Motor':
                    self.env['insurance.quotation'].search([('id', '=', id.id)]).calculate_motor_price()
                elif self.env['insurance.quotation'].search([('id', '=', id.id)]).lob.line_of_business == 'Medical':
                    if data['family_age']:
                        for rec in self.env['medical.family'].search([('application_id', '=', id.id)]):
                            rec.unlink()
                        for rec in data['family_age']:
                            f = self.env['medical.family'].create(
                                {'name': rec['name'], 'DOB': rec['dob'],
                                 'type': rec['type'],
                                 'gender': rec['gender'], 'application_id': id.id})

                            self.env['medical.family'].search([('id', '=', f.id)]).get_age()

                    self.env['insurance.quotation'].search([('id', '=', id.id)]).calculate_price()
                # self.env['insurance.quotation'].search([('id', '=', id.id)]).compute_application_number()
                self.env['insurance.quotation'].search([('id', '=', id.id)]).get_questions()
                record = self.env['insurance.quotation'].search_read([('id', '=', id.id)])

                return {'steps': states, 'app': record}

        else:
            id = self.env['insurance.quotation'].create({'lob': data['lob'],'product_id': data['product_id'],
                                                'name': data['name'], 'phone': data['phone'], 'email': data['email'],
                                                  'test_state': self.env['state.setup'].search([('state', '=', 'Request For Offer')]).id,'state': 'proposal',  'target_price': data['target_price']})
            record = self.env['insurance.quotation'].search_read([('id', '=', id.id)])
        return {'steps': states, 'app': record}
    @api.model
    def get_insurance_app_list(self, parms):
        if parms['app_num']:
            domain = [('create_uid', '=', parms['id']), ('application_number', 'ilike', parms['app_num'])]
        else:
            domain = [('create_uid', '=', parms['id'])]
        return {
            'apps': self.env['insurance.quotation'].search_read(domain, limit=parms['limit'], offset=parms['offset']),
            'count': self.env['insurance.quotation'].search_count(domain)}

    @api.model
    def approve_price(self,id):
        self.env['insurance.quotation'].search([('id', '=', id)]).write(
            {'test_state': self.env['state.setup'].search([('status', '=', 'proposal'),
                                                           ('type', '=', 'insurance_app')]).id,
             'quote_state': 'accepted', 'request_for_ofer_state': 'pending', 'state': 'proposal'})
        self.env['state.history'].create({"application_id": id, "state": 'quick_quote', 'sub_state': 'accepted',
                                          "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                          "user": self.env['insurance.quotation'].search([('id', '=', id)]).write_uid.id})
        self.env['state.history'].create({"application_id": id, "state": 'proposal', 'sub_state': 'pending',
                                          "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                          "user": self.env['insurance.quotation'].search([('id', '=', id)]).write_uid.id})
        return True



    @api.model
    def reject_price(self, id):
        self.env['insurance.quotation'].search([('id', '=', id)]).write({'quote_state': 'cancel'})
        self.env['state.history'].create({"application_id": id, "state": 'quick_quote', 'sub_state': 'cancel',
                                          "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                          "user": self.env['insurance.quotation'].search(
                                              [('id', '=', id)]).write_uid.id})
        return True


    @api.model
    def get_app_info(self, id):
        # return id
        document = []
        # status = []
        offers = []
        state_id = self.env['insurance.quotation'].search([('id', '=', id)]).test_state.id
        rec = self.env['insurance.quotation'].search_read([('id', '=', id)])
        for rec in self.env['state.setup'].search([('id', '=', state_id)]):
            message = rec.message
        rec[0]['message'] = message
        # for record in self.env['state.setup'].search([('product_ids', 'in', [product]),
        #                                               ('type', '=', 'insurance_app'),
        #                                               ('state_for', '=', 'broker')]):
        #     status.append({"name": record.state, "message": record.message})
        for offer in self.env['insurance.quotation'].search([('id', '=', id)]).offer_ids:
            ids = []
            if offer.offer_state != "pending":

                for file in offer.file:
                    ids.append(file.id)

                offers.append({"id": offer.id,"file_id": ids, "type": dict(offer._fields['type'].selection).get(offer.type),
                               "state": offer.offer_state})

        for doc in self.env['insurance.quotation'].search([('id', '=', id)]).final_application_ids:
            description = self.env['final.application.setup'].search([("id", "=", doc.description.id)]).description
            document.append({"id": doc.id, "file_id": doc.application_files.ids, "state": doc.issue_in_progress_state, "attachment": description})


        return {'app': rec, 'offers': offers, "attachment": document}

    @api.model
    def accept_offer(self,id):
        offer = self.env['final.offer'].search([('id', '=', id)])
        for rec in offer:
            rec.write({'offer_state': 'accepted'})
        return True

    @api.model
    def reject_offer(self, id):
        offer = self.env['final.offer'].search([('id', '=', id)])
        for rec in offer:
            rec.write({'offer_state': 'cancel'})
        return True
        # self.env['final.offer'].search([('id', '=', id)])[0].write({'type': ''})
        # return True






