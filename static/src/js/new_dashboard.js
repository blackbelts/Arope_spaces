odoo.define('arope_dashboard.AropeDashboard', function (require) {
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
    template: 'AropeDashboardMain',
    cssLibs: [
      '/Arope-spaces/static/src/css/lib/nv.d3.css'
    ],
    jsLibs: [
      '/Arope-spaces/static/src/js/lib/d3.min.js'
    ],
    events: {
        'click #broker': 'brokerDashboard',
        'click #customer': 'customerDashboard',
        'click #surveyor': 'surveyorDashboard'
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
        console.log("self.multiGroups",self.broker && self.client)
           if(self.multiGroups){
               if((self.broker && self.client))
                   self.$('.o_hr_dashboard').prepend(QWeb.render("arope", {
                        widget: self
                   }));
               else
                self.brokerDashboard()
           }
           else
              self.brokerDashboard()
      })
      return this._super().then(function () {})
    },
    fetch_data: function () {
      var user = session.uid
      var self = this;
      self.broker=false
      self.client=false
      self.surveyor=false
      self.manager=false
      self.multiGroups=true
      var get_dashboard = rpc.query({
        model: "arope.broker",
        method: "get_user_groups",
        args: [user]
      }).then(function (res) {
        self.groups = res.groups
        console.log("res.length==1",res.length)
        if(res.groups.length==1)
            self.multiGroups=false
        console.log("res.length==1",res.length,self.multiGroups)
        for(let i=0;i<res.groups.length;i++){
            if(res.groups[i]=="Broker")
                self.broker=true
            else if  (res.groups[i]=="Client"){
                if(!res.customer){
                    self.client=false
                }else{
                    self.client=true
                }
            }
            else if  (res.groups[i]=="Surveyor")
                self.surveyor=true
            else if  (res.groups[i]=="manager")
                self.manager=true
        }
        console.log("get_dashboard", res,self)
      });
      return $.when(get_dashboard);
    },
    makeNumber: function (x) {
      return parseFloat(x).toFixed(2).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")
    },
     brokerDashboard: function (x) {
      var self = this;
      this.do_action({
        type: "ir.actions.client",
        name: _t('BrokerDashboard '),
        tag: 'broker_dashboard',
      })
    },
     customerDashboard: function (x) {
      var self = this;
      this.do_action({
        type: "ir.actions.client",
        name: _t('CustomerDashboard'),
        tag: 'customer_dashboard',
      })
    },
    surveyorDashboard:function(x){
     var self = this;
      this.do_action({
        type: "ir.actions.client",
        name: _t('SurveyorDashboard'),
        tag: 'surveyor_dashboard',
      })
    }
  });
  core.action_registry.add('arope_dashboard', HrDashboard);
  return HrDashboard;
});