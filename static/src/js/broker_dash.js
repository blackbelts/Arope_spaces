odoo.define('broker_dashboard.BrokerDashboard', function (require) {
  "use strict";
  var AbstractAction = require('web.AbstractAction');
  var ajax = require('web.ajax');
  var core = require('web.core');
  var rpc = require('web.rpc');
  var session = require('web.session');
  var web_client = require('web.web_client');
  var _t = core._t;
  var QWeb = core.qweb;
  var BrokerDashboard = AbstractAction.extend({
    template: 'BrokerDashboardMain',
    cssLibs: [
      '/Arope_spaces/static/src/css/lib/nv.d3.css'
    ],
    jsLibs: [
      '/Arope_spaces/static/src/js/lib/d3.min.js'
    ],
    events: {
        'click #policies': 'policies_list',
        'click #renewals': 'renewals_list',
        'click #collections':'collections_list',
        'click #complaints': 'complaints_list',
        'click #claims':'claims_list',
        'click #endorsement':'end_request_list',
        'click #cancellation': 'cancel_request_list',
        'click #renewals-req':'renewals_request_list',
        'click #button1':'showDash1',
        'click #button2':'showDash2',
        'click #button3':'showDash3',
        'click #button4':'showDash4',
        'click #button5':'showDash5',
        'click #button6':'showDash6',
        'click #button7':'showDash7',
        'click #button8':'showDash8',
        'click #apps':'insuranceApps',
        'click #insuranceApp':'insuranceApps',
        'click #travel':'travel',
        'click #pa':'personalAcc',




    },
    init: function (parent, context) {
      this._super(parent, context);
      this.action_id = context.id;
      this._super(parent, context);
    },
    start: function () {
      var user = session.uid
      var self = this;
      this.fetch_data().then(function(){

      self.$('.o_hr_dashboard').prepend(QWeb.render("brokerdash", {
            widget: self
          }));
//          this.showDash1()
          $("document").ready(function () {
            var dataProvider = []
            var monthes = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            self.target_production.target.forEach(function (e, i) {
              var dataProvideritem = {}
              dataProvideritem.month = monthes[i]
              dataProvideritem.target = e.toFixed(2)
              dataProvideritem.production = self.target_production.production[i].toFixed(2)
              dataProvideritem.color = "#3778C2"
              dataProvider.push(dataProvideritem)
            })
            var chart = AmCharts.makeChart("ambarchart2", {
              "theme": "light",
              "type": "serial",
              "balloon": {
                "adjustBorderColor": false,
                "horizontalPadding": 10,
                "verticalPadding": 4,
                "color": "#fff"
              },
              "dataProvider": dataProvider,
              "valueAxes": [{
                /*"unit": "EGP",*/
                "position": "left",
              }],
              "startDuration": 1,
              "graphs": [{
                "alphaField": "alpha",
                "balloonText": "<span style='font-size:12px;'>[[title]] in [[category]]:<br><span style='font-size:20px;'>[[value]]</span> [[additional]]</span>",
                "fillAlphas": 1,
                "fillColorsField": "color",
                "title": "Production",
                "type": "column",
                "valueField": "production",
                "dashLengthField": "dashLengthColumn"
              }, {
                "id": "graph2",
                "balloonText": "<span style='font-size:12px;'>[[title]] in [[category]]:<br><span style='font-size:20px;'>[[value]]</span> [[additional]]</span>",
                "bullet": "round",
                "lineThickness": 3,
                "bulletSize": 7,
                "bulletBorderAlpha": 1,
                "bulletColor": "#FFFFFF",
                "lineColor": "#3EB650",
                "useLineColorForBulletBorder": true,
                "bulletBorderThickness": 3,
                "fillAlphas": 0,
                "lineAlpha": 1,
                "title": "Target",
                "valueField": "target",
                "dashLengthField": "dashLengthLine"
              }],
              "plotAreaFillAlphas": 0.1,
              "categoryField": "month",
              "categoryAxis": {
                "gridPosition": "start"
              },
              "export": {
                "enabled": false
              }

            });
            var dataProvider2 = []
            self.production_compare.current_year.forEach(function (e, i) {
              var dataProvideritem = {}
              dataProvideritem.month = monthes[i]
              dataProvideritem.current_year = e.toFixed(2)
              dataProvideritem.last_year = self.production_compare.last_year[i].toFixed(2)
              dataProvideritem.color = "#3EB650"
              dataProvideritem.color2 = "#3778C2"
              dataProvider2.push(dataProvideritem)
            })
            var chart = AmCharts.makeChart("ambarchart1", {
              "theme": "light",
              "type": "serial",
              "balloon": {
                "adjustBorderColor": false,
                "horizontalPadding": 10,
                "verticalPadding": 4,
                "color": "#fff"
              },
              "dataProvider": dataProvider2,
              "valueAxes": [{
                /*"unit": "EGP",*/
                "position": "left",
              }],
              "startDuration": 1,
              "graphs": [{
                "balloonText": "production in [[category]] (current year): <b>[[value]]</b>",
                "fillAlphas": 0.9,
                "fillColorsField": "color",
                "lineAlpha": 0.2,
                "title": "current Year",
                "type": "column",
                "valueField": "current_year"
              }, {
                "balloonText": "production in [[category]] (last year) <b>[[value]]</b>",
                "fillAlphas": 0.9,
                "fillColorsField": "color2",
                "lineAlpha": 0.2,
                "title": "2018",
                "type": "column",
                "clustered": false,
                "columnWidth": 0.5,
                "valueField": "last_year"
              }],
              "plotAreaFillAlphas": 0.1,
              "categoryField": "month",
              "categoryAxis": {
                "gridPosition": "start"
              },
              "export": {
                "enabled": false
              }

            });
            var lobs=[]
            console.log(self.policy_lob)
            if(self.policy_lob != false){
                console.log("ifffffffffff")
                self.policy_lob.forEach(function(e){
                    lobs.push({
                        title:e.name,
                        value:e.amount
                    })
                })
            }else{
            console.log("elseeeeeeeeeeeee")
            }

            var piechart = AmCharts.makeChart("ambarchart3", {
              "type": "pie",
              "labelRadius": -35,
              "theme": "light",
              "legend":{
                "position":"right"
              },
              colors: ["#FCC133", "#3EB650", "#3EB650","#3778C2","#292930"],
              "labelText": "",
              "dataProvider": lobs,
              "titleField": "title",
              "valueField": "value",
              "export": {
                "enabled": false
              },
              "color": "blue"
            });
          })
      })
//      this.showDash1()
      return this._super().then(function () {})
    },
    fetch_data: function () {
      var user = session.uid
      var self = this;
      var context
       if(self.controlPanelParams.context.user_id == undefined ){
            console.log("if")
            context= JSON.parse(localStorage.getItem('context'))
       }
       else{
            console.log("else")
            localStorage.setItem('context', JSON.stringify(self.controlPanelParams.context));
            context = self.controlPanelParams.context
       }
       console.log(context)
       console.log("contextcontextcontextcontextcontext",context)

      var get_dashboard = rpc.query({
        model: "arope.broker",
        method: "get_broker_dashboard",
        args: [context.user_id]
      }).then(function (res) {
        self.brokerProduction = res.production
        self.target_production = res.targetVsProduction
        self.brokerRank = res.rank
        self.collections_statistics = res.collections
        self.renew_statistics = res.renews
        self.production_compare = res.lastVsCurrentYear
        self.user = res.user
        self.collection_ratio=res.collection_ratio
        self.claims_ratio=res.claims_ratio
        self.policy_lob=res.policy_lob
        self.claim_lob=res.claim_lob
        self.App_count=res.App_count
        self.user_image=res.user_image
        self.renew_request=res.renew_request
        self.cancel_request=res.cancel_request
        self.end_request=res.end_request
        self.customers = res.customers
        res.complaint_count.forEach(function(e,i){
            if(e.stage=="Canceled")
                res.complaint_count.splice(i,1)
            else if(e.stage=="New"){
                e.image="/Arope_spaces/static/src/img/red.png"
                e.subClass="redspan"
            }
            else if(e.stage=="Solved"){
                e.image="/Arope_spaces/static/src/img/green.png"
                e.subClass="greenspan"
            }
            else{
                 e.image="/Arope_spaces/static/src/img/orange.png"
                 e.subClass="orangespan"
            }
        })
        self.complaint_count=res.complaint_count
        //                self.collections_statistics=res
        console.log("get_dashboard", res)
      });
      return $.when(get_dashboard);
    },
    showDash1: function(){
      var button1 = document.getElementById("button1");
      var button2 = document.getElementById("button2");
      var button3 = document.getElementById("button3");
      var button4 = document.getElementById("button4");
      var button5 = document.getElementById("button5");
      var button6 = document.getElementById("button6");
      var button7 = document.getElementById("button7");
      button1.setAttribute('style', 'background: linear-gradient(150deg, #073e89 20%, #073e89 80%) !important;color: white !important;');
      button2.setAttribute('style', 'background: white !important;color: darkblue !important;');
      button3.setAttribute('style', 'background: white !important;color: darkblue !important;');
      button4.setAttribute('style', 'background: white !important;color: darkblue !important;');
      button5.setAttribute('style', 'background: white !important;color: darkblue !important;');
      button6.setAttribute('style', 'background: white !important;color: darkblue !important;');
      button7.setAttribute('style', 'background: white !important;color: darkblue !important;');
      var dash1 = document.getElementById("dash1");
      var dash2 = document.getElementById("dash2");
      var dash3 = document.getElementById("dash3");
      var dash4 = document.getElementById("dash4");
      var dash5 = document.getElementById("dash5");
      var dash6 = document.getElementById("dash6");
      var dash7 = document.getElementById("dash7");
      dash1.setAttribute('style', 'display:flex !important');
      dash2.setAttribute('style', 'display:none !important');
      dash3.setAttribute('style', 'display:none !important');
      dash4.setAttribute('style', 'display:none !important');
      dash5.setAttribute('style', 'display:none !important');
      dash6.setAttribute('style', 'display:none !important');
      dash7.setAttribute('style', 'display:none !important');


    },
    showDash2: function(){
      var button1 = document.getElementById("button1");
      var button2 = document.getElementById("button2");
      var button3 = document.getElementById("button3");
      var button4 = document.getElementById("button4");
      var button5 = document.getElementById("button5");
      var button6 = document.getElementById("button6");
      var button7 = document.getElementById("button7");
      button2.setAttribute('style', 'background: linear-gradient(150deg, #073e89 20%, #073e89 80%) !important;color: white !important;');
      button1.setAttribute('style', 'background: white !important;color: darkblue !important;');
      button3.setAttribute('style', 'background: white !important;color: darkblue !important;');
      button4.setAttribute('style', 'background: white !important;color: darkblue !important;');
      button5.setAttribute('style', 'background: white !important;color: darkblue !important;');
      button6.setAttribute('style', 'background: white !important;color: darkblue !important;');
      button7.setAttribute('style', 'background: white !important;color: darkblue !important;');
      var dash1 = document.getElementById("dash1");
      var dash2 = document.getElementById("dash2");
      var dash3 = document.getElementById("dash3");
      var dash4 = document.getElementById("dash4");
      var dash5 = document.getElementById("dash5");
      var dash6 = document.getElementById("dash6");
      var dash7 = document.getElementById("dash7");
      dash1.setAttribute('style', 'display:none !important');
      dash2.setAttribute('style', 'display:flex !important');
      dash3.setAttribute('style', 'display:none !important');
      dash4.setAttribute('style', 'display:none !important');
      dash5.setAttribute('style', 'display:none !important');
      dash6.setAttribute('style', 'display:none !important');
      dash7.setAttribute('style', 'display:none !important');

    },
    showDash3: function(){
      var button1 = document.getElementById("button1");
      var button2 = document.getElementById("button2");
      var button3 = document.getElementById("button3");
      var button4 = document.getElementById("button4");
      var button5 = document.getElementById("button5");
      var button6 = document.getElementById("button6");
      var button7 = document.getElementById("button7");
      button3.setAttribute('style', 'background: linear-gradient(150deg, #073e89 20%, #073e89 80%) !important;color: white !important;');
      button2.setAttribute('style', 'background: white !important;color: darkblue !important;');
      button1.setAttribute('style', 'background: white !important;color: darkblue !important;');
      button4.setAttribute('style', 'background: white !important;color: darkblue !important;');
      button5.setAttribute('style', 'background: white !important;color: darkblue !important;');
      button6.setAttribute('style', 'background: white !important;color: darkblue !important;');
      button7.setAttribute('style', 'background: white !important;color: darkblue !important;');
      var dash1 = document.getElementById("dash1");
      var dash2 = document.getElementById("dash2");
      var dash3 = document.getElementById("dash3");
      var dash4 = document.getElementById("dash4");
      var dash5 = document.getElementById("dash5");
      var dash6 = document.getElementById("dash6");
      var dash7 = document.getElementById("dash7");
      dash1.setAttribute('style', 'display:none !important');
      dash2.setAttribute('style', 'display:none !important');
      dash3.setAttribute('style', 'display:flex !important');
      dash4.setAttribute('style', 'display:none !important');
      dash5.setAttribute('style', 'display:none !important');
      dash6.setAttribute('style', 'display:none !important');
      dash7.setAttribute('style', 'display:none !important');
    },
    showDash4: function(){
      this.do_action({
        name: _t("Customers"),
        type: 'ir.actions.act_window',
        res_model: 'persons',
        view_mode: 'tree',
        views: [
          [2000, 'list']
        ],
        domain: [
          ['id', 'in', this.customers]
        ],context:{
            "edit":false,
            "create":false
        },
        target: 'current'
      })
    },
    showDash5: function(){

//      var dash1 = document.getElementById("dash1");
//      var dash2 = document.getElementById("dash2");
//      var dash3 = document.getElementById("dash3");
//      var dash4 = document.getElementById("dash4");
//      var dash5 = document.getElementById("dash5");
//      var dash6 = document.getElementById("dash6");
//      var dash7 = document.getElementById("dash7");
//      dash1.setAttribute('style', 'display:none !important');
//      dash2.setAttribute('style', 'display:none !important');
//      dash3.setAttribute('style', 'display:none !important');
//      dash4.setAttribute('style', 'display:none !important');
//      dash5.setAttribute('style', 'display:flex !important');
//      dash6.setAttribute('style', 'display:none !important');
//      dash7.setAttribute('style', 'display:none !important');
    console.log("policies")
      var self = this;
      this.do_action({
        name: "Motor Claims",
        type: 'ir.actions.act_window',
        res_model: 'crm.lead',
        view_mode: 'tree,form',
        views: [
          [false, 'list'],[false, 'form']
        ],
        domain: [
          ['opp_type', '=', 4],
          ['create_uid', '=', this.user.id]
        ],
        context:{
            'default_type': 'opportunity',
            'default_opp_type': 4
        },
        target: 'current'
      })

    },
    showDash6: function(){

      var self = this;
      this.do_action({
        name: "General Claims",
        type: 'ir.actions.act_window',
        res_model: 'crm.lead',
        view_mode: 'tree,form',
        views: [
          [false, 'list'],[false, 'form']
        ],
        domain: [
          ['opp_type', '=', 3],
          ['create_uid', '=', this.user.id]
        ],
        context:{
            'default_type': 'opportunity',
            'default_opp_type': 3
        },
        target: 'current'
      })

    },
    showDash7: function(){
      var button1 = document.getElementById("button1");
      var button2 = document.getElementById("button2");
      var button3 = document.getElementById("button3");
      var button4 = document.getElementById("button4");
      var button5 = document.getElementById("button5");
      var button6 = document.getElementById("button6");
      var button7 = document.getElementById("button7");
      button7.setAttribute('style', 'background: linear-gradient(150deg, #073e89 20%, #073e89 80%) !important;color: white !important;width: 13.8%;');
      button2.setAttribute('style', 'background: white !important;color: darkblue !important;');
      button3.setAttribute('style', 'background: white !important;color: darkblue !important;');
      button4.setAttribute('style', 'background: white !important;color: darkblue !important;');
      button5.setAttribute('style', 'background: white !important;color: darkblue !important;');
      button6.setAttribute('style', 'background: white !important;color: darkblue !important;');
      button1.setAttribute('style', 'background: white !important;color: darkblue !important;');
      var dash1 = document.getElementById("dash1");
      var dash2 = document.getElementById("dash2");
      var dash3 = document.getElementById("dash3");
      var dash4 = document.getElementById("dash4");
      var dash5 = document.getElementById("dash5");
      var dash6 = document.getElementById("dash6");
      var dash7 = document.getElementById("dash7");
      dash1.setAttribute('style', 'display:none !important');
      dash2.setAttribute('style', 'display:none !important');
      dash3.setAttribute('style', 'display:none !important');
      dash4.setAttribute('style', 'display:none !important');
      dash5.setAttribute('style', 'display:none !important');
      dash6.setAttribute('style', 'display:none !important');
      dash7.setAttribute('style', 'display:flex !important');

    },
    showDash8: function(){

      var self = this;
      this.do_action({
        name: "Quick Quote",
        type: 'ir.actions.act_window',
        res_model: 'quotation.service',
        view_mode: 'tree,form',
        views: [
          [false, 'list'],[false, 'form']
        ],
        domain: [
//          ['opp_type', '=', 3],
          ['create_uid', '=', this.user.id]
        ],
//        context:{
//            'default_type': 'opportunity',
//            'default_opp_type': 3
//        },
        target: 'current'
      })

    },
    makeNumber: function (x) {
      return parseFloat(x).toFixed(2).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")
    },
    policies_list: function (x) {
      console.log("policies")
      var self = this;
      this.do_action({
        name: _t("Policy Tree"),
        type: 'ir.actions.act_window',
        res_model: 'policy.arope',
        view_mode: 'tree',
        views: [
          [2001, 'list']
        ],
        domain: [
          ['id', 'in', this.brokerProduction.ids]
        ],context:{
            "edit":false,
            "create":false
        },
        target: 'current'
      })
    },
    renewals_list: function (x) {
      /*var self = this;*/
      var idsList=[]
      idsList=idsList.concat(this.renew_statistics.Green.ids,this.renew_statistics.Orange.ids,this.renew_statistics.Red.ids)
      console.log("idsList",idsList)
      this.do_action({
        name: _t("Policy Tree"),
        type: 'ir.actions.act_window',
        res_model: 'policy.arope',
        view_mode: 'tree',
        views: [
          [2001, 'list']
        ],
        domain: [
          ['id', 'in', idsList]
        ],
        context:{
            "edit":false,
            "create":false
        },
        target: 'current'
      })
    },
    collections_list: function (x) {
      /*var self = this;*/
      var idsList=[]
      idsList=idsList.concat(this.collections_statistics.Green.ids,this.collections_statistics.Orange.ids,this.collections_statistics.Red.ids)
      console.log("idsList",idsList)
      this.do_action({
        name: _t("tree.collection"),
        type: 'ir.actions.act_window',
        res_model: 'collection.arope',
        view_mode: 'tree',
        views: [
          [false, 'list']
        ],
        domain: [
          ['id', 'in', idsList]
        ],
        context:{
            "edit":false,
            "create":false
        },
        target: 'current'
      })
    },
    complaints_list:function (x) {
      /*var self = this;*/
      var idsList=[]
      this.complaint_count.forEach(function(item){
        idsList=idsList.concat(item.ids)
      })
      console.log("complaints_list",idsList)
      this.do_action({
        name: _t("Complaint"),
        type: 'ir.actions.act_window',
        res_model: 'helpdesk_lite.ticket',
        view_mode: 'tree',
        views: [
          [false, 'list'],[false, 'form']
        ],
        domain: [
          ['id', 'in', idsList]
        ],
        context:{
            "edit":false,
            "create":false
        },
        target: 'current'
      })
    },
    claims_list:function (x) {
      var idsList=[]
      this.claim_lob.forEach(function(item){
        idsList=idsList.concat(item.ids)
      })
      console.log("complaints_list",idsList)
      this.do_action({
        name: _t("Claims Tree"),
        type: 'ir.actions.act_window',
        res_model: 'claim.arope',
        view_mode: 'tree',
        views: [
          [false, 'list']
        ],
        domain: [
          ['id', 'in', idsList]
        ],
        context:{
            "edit":false,
            "create":false
        },
        target: 'current'
      })
    },
     end_request_list:function (x) {
      this.do_action({
       name: _t("Requests"),
        type: 'ir.actions.act_window',
        res_model: 'crm.lead',
        view_mode: 'form,tree',
        views: [
          [false, 'list'],[false, 'form']
        ],
        domain: [
          ['type','=','opportunity'],
          ['opp_type','=', 2],
          ['policy_services_type', '=', 'end'],
          ['create_uid', '=', this.user.id]
        ],
        context:{
            'default_type': 'opportunity',
            'default_opp_type': 2
        },
        target: 'current'
      })
    },

    insuranceApps:function (x) {
      this.do_action({

        name: _t("Insurance Application"),
        type: 'ir.actions.act_window',
        res_model: 'crm.lead',
        view_mode: 'tree,form',
        views: [
          [false, 'list'],[false, 'form']
        ],
        domain: [
          ['type','=','opportunity'],
          ['opp_type','=',1],
          ['create_uid', '=', this.user.id]
        ],
        context:{
            'default_type': 'opportunity',
            'default_opp_type': 1,
            "edit":true,
            "create":true
        },
        target: 'current'
      })
    },
    travel:function (x) {
      this.do_action({

        name: _t("Travel"),
        type: 'ir.actions.act_window',
        res_model: 'policy.travel',
        view_mode: 'tree,form',
        views: [
          [false, 'list'],[false, 'form']
        ],
        domain: [
          ['create_uid', '=', this.user.id]
        ],
        context:{

            "edit":true,
            "create":true
        },
        target: 'current'
      })
    },
    personalAcc:function (x) {
      this.do_action({

        name: _t("Personal Accident"),
        type: 'ir.actions.act_window',
        res_model: 'policy.personal',
        view_mode: 'tree,form',
        views: [
          [false, 'list'],[false, 'form']
        ],
        domain: [
          ['create_uid', '=', this.user.id]
        ],
        context:{

            "edit":true,
            "create":true
        },
        target: 'current'
      })
    },
     cancel_request_list:function (x) {
      this.do_action({
       name: _t("Requests"),
        type: 'ir.actions.act_window',
        res_model: 'crm.lead',
        view_mode: 'form,tree',
        views: [
          [false, 'list'],[false, 'form']
        ],
        domain: [
          ['type','=','opportunity'],
          ['opp_type','=', 2],
          ['policy_services_type', '=', 'cancel'],
          ['create_uid', '=', this.user.id]
        ],
        context:{
            'default_type': 'opportunity',
            'default_opp_type': 2
        },
        target: 'current'
      })
    },
     renewals_request_list:function (x) {
      this.do_action({
       name: _t("Requests"),
        type: 'ir.actions.act_window',
        res_model: 'crm.lead',
        view_mode: 'form,tree',
        views: [
          [false, 'list'],[false, 'form']
        ],
        domain: [
          ['type','=','opportunity'],
          ['opp_type','=', 2],
          ['policy_services_type', '=', 'renew'],
          ['create_uid', '=', this.user.id]
        ],
        context:{
            'default_type': 'opportunity',
            'default_opp_type': 2
        },
        target: 'current'
      })
    },

  });
  core.action_registry.add('broker_dashboard', BrokerDashboard);
  return BrokerDashboard;
});