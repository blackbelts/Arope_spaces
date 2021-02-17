odoo.define('customer_dashboard.CustomerDashboard', function (require) {
  "use strict";
  var AbstractAction = require('web.AbstractAction');
  var ajax = require('web.ajax');
  var core = require('web.core');
  var rpc = require('web.rpc');
  var session = require('web.session');
  var web_client = require('web.web_client');
  var _t = core._t;
  var QWeb = core.qweb;

  var CustomerDashboard = AbstractAction.extend({
    template: 'CustomerDashboardMain',
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
        'click #button2':'showDash2',
        'click #button3':'showDash3',
        'click #button5':'showDash5',
        'click #button6':'showDash6',
        'click #button7':'showDash7',
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
        self.$('.o_hr_dashboard').prepend(QWeb.render("customerdash", {
            widget: self
          }));
      })
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
      var get_dashboard = rpc.query({
        model: "arope.broker",
        method: "get_customer_dashboard",
        args: [context.user_id]
      }).then(function (res) {
        /*self.target_production = res.targetVsProduction
        self.brokerRank = res.rank
        self.production_compare = res.lastVsCurrentYear*/
        self.collections_statistics = res.collections
        self.renew_statistics = res.renews
        self.App_count=res.App_count
        self.cancel_request=res.cancel_request
        self.claim_lob=res.claim_lob
        self.claims_ratio=res.claims_ratio
        self.collection_ratio=res.collection_ratio
        self.complaint_count=res.complaint_count
        self.end_request=res.end_request
        self.policy_lob=res.policy_lob
        self.brokerProduction = res.production
        self.renew_request=res.renew_request
        self.user = res.user
        self.user_image=res.user_image
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
        console.log("get_customer_dashboard", res)
      });
      return $.when(get_dashboard);
    },
    showDash2: function(){

      var button2 = document.getElementById("button2");
      var button3 = document.getElementById("button3");
      var button5 = document.getElementById("button5");
      var button6 = document.getElementById("button6");
      var button7 = document.getElementById("button7");
      button2.setAttribute('style', 'background: linear-gradient(150deg, #073e89 20%, #073e89 80%) !important;color: white !important;');
      button3.setAttribute('style', 'background: white !important;color: darkblue !important;');
      button5.setAttribute('style', 'background: white !important;color: darkblue !important;');
      button6.setAttribute('style', 'background: white !important;color: darkblue !important;');
      button7.setAttribute('style', 'background: white !important;color: darkblue !important;');

      var dash2 = document.getElementById("dash2");
      var dash3 = document.getElementById("dash3");
      var dash5 = document.getElementById("dash5");
      var dash6 = document.getElementById("dash6");
      var dash7 = document.getElementById("dash7");
      dash2.setAttribute('style', 'display:flex !important');
      dash3.setAttribute('style', 'display:none !important');
      dash5.setAttribute('style', 'display:none !important');
      dash6.setAttribute('style', 'display:none !important');
      dash7.setAttribute('style', 'display:none !important');

    },
    showDash3: function(){
      var button2 = document.getElementById("button2");
      var button3 = document.getElementById("button3");
      var button5 = document.getElementById("button5");
      var button6 = document.getElementById("button6");
      var button7 = document.getElementById("button7");
      button3.setAttribute('style', 'background: linear-gradient(150deg, #073e89 20%, #073e89 80%) !important;color: white !important;');
      button2.setAttribute('style', 'background: white !important;color: darkblue !important;');
      button5.setAttribute('style', 'background: white !important;color: darkblue !important;');
      button6.setAttribute('style', 'background: white !important;color: darkblue !important;');
      button7.setAttribute('style', 'background: white !important;color: darkblue !important;');
      var dash2 = document.getElementById("dash2");
      var dash3 = document.getElementById("dash3");
      var dash5 = document.getElementById("dash5");
      var dash6 = document.getElementById("dash6");
      var dash7 = document.getElementById("dash7");
      dash2.setAttribute('style', 'display:none !important');
      dash3.setAttribute('style', 'display:flex !important');
      dash5.setAttribute('style', 'display:none !important');
      dash6.setAttribute('style', 'display:none !important');
      dash7.setAttribute('style', 'display:none !important');
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
          [false, 'list']
        ],
        domain: [
          ['opp_type', '=', 4]
        ],
        target: 'current'
      })

    },
    showDash6: function(){
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
//      dash5.setAttribute('style', 'display:none !important');
//      dash6.setAttribute('style', 'display:flex !important');
//      dash7.setAttribute('style', 'display:none !important');
      console.log("policies")
      var self = this;
      this.do_action({
        name: "General Claims",
        type: 'ir.actions.act_window',
        res_model: 'crm.lead',
        view_mode: 'tree,form',
        views: [
          [false, 'list']
        ],
        domain: [
          ['opp_type', '=', 3]
        ],
        target: 'current'
      })

    },
    showDash7: function(){
      var button2 = document.getElementById("button2");
      var button3 = document.getElementById("button3");
      var button5 = document.getElementById("button5");
      var button6 = document.getElementById("button6");
      var button7 = document.getElementById("button7");
      button7.setAttribute('style', 'background: linear-gradient(150deg, #073e89 20%, #073e89 80%) !important;color: white !important;width: 13.8%;');
      button2.setAttribute('style', 'background: white !important;color: darkblue !important;');
      button3.setAttribute('style', 'background: white !important;color: darkblue !important;');
      button5.setAttribute('style', 'background: white !important;color: darkblue !important;');
      button6.setAttribute('style', 'background: white !important;color: darkblue !important;');
      var dash2 = document.getElementById("dash2");
      var dash3 = document.getElementById("dash3");
      var dash5 = document.getElementById("dash5");
      var dash6 = document.getElementById("dash6");
      var dash7 = document.getElementById("dash7");
      dash2.setAttribute('style', 'display:none !important');
      dash3.setAttribute('style', 'display:none !important');
      dash5.setAttribute('style', 'display:none !important');
      dash6.setAttribute('style', 'display:none !important');
      dash7.setAttribute('style', 'display:flex !important');

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
  core.action_registry.add('customer_dashboard', CustomerDashboard);
  return CustomerDashboard;
});