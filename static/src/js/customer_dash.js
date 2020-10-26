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
      '/Arope-spaces/static/src/css/lib/nv.d3.css'
    ],
    jsLibs: [
      '/Arope-spaces/static/src/js/lib/d3.min.js'
    ],
    events: {
      /*'click #production': 'production_list',*/
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
      var get_dashboard = rpc.query({
        model: "arope.broker",
        method: "get_customer_dashboard",
        args: [user]
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
        self.user = res.user[0]
        self.user_image=res.user_image
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
        console.log("get_customer_dashboard", res)
      });
      return $.when(get_dashboard);
    },
    makeNumber: function (x) {
      return parseFloat(x).toFixed(2).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")
    },
  });
  core.action_registry.add('customer_dashboard', CustomerDashboard);
  return CustomerDashboard;
});