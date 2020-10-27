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
      '/Arope-spaces/static/src/css/lib/nv.d3.css'
    ],
    jsLibs: [
      '/Arope-spaces/static/src/js/lib/d3.min.js'
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
            self.policy_lob.forEach(function(e){
                lobs.push({
                    title:e.name,
                    value:e.amount
                })
            })
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
      return this._super().then(function () {})
    },
    fetch_data: function () {
      var user = session.uid
      var self = this;
      var get_dashboard = rpc.query({
        model: "arope.broker",
        method: "get_broker_dashboard",
        args: [self.controlPanelParams.context.user_id]
      }).then(function (res) {
        self.brokerProduction = res.production
        self.target_production = res.targetVsProduction
        self.brokerRank = res.rank
        self.collections_statistics = res.collections
        self.renew_statistics = res.renews
        self.production_compare = res.lastVsCurrentYear
        self.user = res.user[0]
        self.collection_ratio=res.collection_ratio
        self.claims_ratio=res.claims_ratio
        self.policy_lob=res.policy_lob
        self.claim_lob=res.claim_lob
        self.App_count=res.App_count
        self.user_image=res.user_image
        self.renew_request=res.renew_request
        self.cancel_request=res.cancel_request
        self.end_request=res.end_request
        res.complaint_count.forEach(function(e,i){
            if(e.stage=="Canceled")
                res.complaint_count.splice(i,1)
            else if(e.stage=="New"){
                e.image="/Arope-spaces/static/src/img/red.png"
                e.subClass="redspan"
            }
            else if(e.stage=="Solved"){
                e.image="/Arope-spaces/static/src/img/green.png"
                e.subClass="greenspan"
            }
            else{
                 e.image="/Arope-spaces/static/src/img/orange.png"
                 e.subClass="orangespan"
            }
        })
        self.complaint_count=res.complaint_count
        //                self.collections_statistics=res
        console.log("get_dashboard", res)
      });
      return $.when(get_dashboard);
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
          [false, 'list']
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
        res_model: 'policy.request',
        view_mode: 'tree',
        views: [
          [false, 'list']
        ],
        domain: [
          ['id', 'in', this.end_request.ids]
        ],
        context:{
            "edit":false,
            "create":false
        },
        target: 'current'
      })
    },
     cancel_request_list:function (x) {
      this.do_action({
        name: _t("Requests"),
        type: 'ir.actions.act_window',
        res_model: 'policy.request',
        view_mode: 'tree',
        views: [
          [false, 'list']
        ],
        domain: [
          ['id', 'in', this.cancel_request.ids]
        ],
        context:{
            "edit":false,
            "create":false
        },
        target: 'current'
      })
    },
     renewals_request_list:function (x) {
      this.do_action({
        name: _t("Requests"),
        type: 'ir.actions.act_window',
        res_model: 'policy.request',
        view_mode: 'tree',
        views: [
          [false, 'list']
        ],
        domain: [
          ['id', 'in', this.renew_request.ids]
        ],
        context:{
            "edit":false,
            "create":false
        },
        target: 'current'
      })
    },

  });
  core.action_registry.add('broker_dashboard', BrokerDashboard);
  return BrokerDashboard;
});