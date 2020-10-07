odoo.define('hrms_dashboard.Dashboard', function (require) {
  "use strict";

  var AbstractAction = require('web.AbstractAction');
  var ajax = require('web.ajax');
  var core = require('web.core');
  var rpc = require('web.rpc');
  var session = require('web.session');
  var web_client = require('web.web_client');
  var _t = core._t;
  var QWeb = core.qweb;

  var HrDashboard = AbstractAction.extend({
    template: 'HrDashboardMain',
    cssLibs: [
      '/Arope-spaces/static/src/css/lib/nv.d3.css'
    ],
    jsLibs: [
      '/Arope-spaces/static/src/js/lib/d3.min.js'
    ],
    events: {

      'click #production': 'production_list',
      'click #green_collection': 'green_collection',
      'click #orange_collection': 'orange_collection',
      'click #red_collection': 'red_collection',
      'click #green_renew': 'green_renew',
      'click #orange_renew': 'orange_renew',
      'click #red_renew': 'red_renew',
    },
    init: function (parent, context) {
      this._super(parent, context);
      this.action_id = context.id;
      this._super(parent, context);

    },
    start: function () {
      var user = session.uid
      var self = this;
      this.fetch_data().then(function () {
        if (self.user.length!=0&&self.user[0].type == "broker") {
          self.$('.o_hr_dashboard').prepend(QWeb.render("broker", {
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
                "unit": "$",
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
                "unit": "$",
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

        } else if (self.user.length!=0&&self.user[0].type == "customer") {
          self.$('.o_hr_dashboard').prepend(QWeb.render("customer", {
            widget: self
          }));
        } else if (self.user.length!=0&&self.user[0].type == "surveyor") {
          self.$('.o_hr_dashboard').prepend(QWeb.render("surveyor", {
            widget: self
          }));
        } else {
          self.$('.o_hr_dashboard').prepend(QWeb.render("general", {
            widget: self
          }));
        }

      })


      return this._super().then(function () {})
    },
    fetch_data: function () {

      var user = session.uid
      var self = this;
      var get_dashboard = rpc.query({
        model: "arope.broker",
        method: "get_dashboard",
        args: [user]
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
        res.complaint_count.forEach(function(e,i){
            if(e.stage=="Canceled")
                res.complaint_count.splice(i,1)
            else if(e.stage=="New"){
                e.class="icon red"
                e.subClass="redspan"
            }
            else if(e.stage=="Solved"){
                e.class="icon green"
                e.subClass="greenspan"
            }
            else{
                 e.class="icon orange"
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
    production_list: function (x) {
      var self = this;
      this.do_action({
        name: _t("Policy Tree"),
        type: 'ir.actions.act_window',
        res_model: 'policy.arope',
        view_mode: 'tree,form,calendar',
        views: [
          [false, 'list'],
          [false, 'form']
        ],
        domain: [
          ['id', 'in', this.brokerProduction.ids]
        ],
        target: 'current'
      })
    },
    green_collection: function () {
      var self = this;
      this.do_action({
        name: _t("tree.collection"),
        type: 'ir.actions.act_window',
        res_model: 'collection.arope',
        view_mode: 'tree,form,calendar',
        views: [
          [false, 'list'],
          [false, 'form']
        ],
        domain: [
          ['id', 'in', this.collections_statistics.Green.ids]
        ],
        target: 'current'
      })
    },
    orange_collection: function () {
      var self = this;
      this.do_action({
        name: _t("tree.collection"),
        type: 'ir.actions.act_window',
        res_model: 'collection.arope',
        view_mode: 'tree,form,calendar',
        views: [
          [false, 'list'],
          [false, 'form']
        ],
        domain: [
          ['id', 'in', this.collections_statistics.Orange.ids]
        ],
        target: 'current'
      })

    },
    red_collection: function () {
      var self = this;
      this.do_action({
        name: _t("tree.collection"),
        type: 'ir.actions.act_window',
        res_model: 'collection.arope',
        view_mode: 'tree,form,calendar',
        views: [
          [false, 'list'],
          [false, 'form']
        ],
        domain: [
          ['id', 'in', this.collections_statistics.Red.ids]
        ],
        target: 'current'
      })
    },
    orange_renew: function () {
      var self = this;
      this.do_action({
        name: _t("Policy Tree"),
        type: 'ir.actions.act_window',
        res_model: 'policy.arope',
        view_mode: 'tree,form,calendar',
        views: [
          [false, 'list'],
          [false, 'form']
        ],
        domain: [
          ['id', 'in', this.renew_statistics.Orange.ids]
        ],
        target: 'current'
      })

    },
    green_renew: function () {
      var self = this;
      this.do_action({
        name: _t("Policy Tree"),
        type: 'ir.actions.act_window',
        res_model: 'policy.arope',
        view_mode: 'tree,form,calendar',
        views: [
          [false, 'list'],
          [false, 'form']
        ],
        domain: [
          ['id', 'in', this.renew_statistics.Green.ids]
        ],
        target: 'current'
      })
    },
    red_renew: function () {
      var self = this;
      this.do_action({
        name: _t("Policy Tree"),
        type: 'ir.actions.act_window',
        res_model: 'policy.arope',
        view_mode: 'tree,form,calendar',
        views: [
          [false, 'list'],
          [false, 'form']
        ],
        domain: [
          ['id', 'in', this.renew_statistics.Red.ids]
        ],
        target: 'current'
      })
    },

  });


  core.action_registry.add('hr_dashboard', HrDashboard);

  return HrDashboard;

});