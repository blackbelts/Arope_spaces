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
                self.$('.o_hr_dashboard').prepend(QWeb.render("HrDashboardMain2", { widget: self }));
                //                console.log(self)
                //                console.log(self.production_compare,self.target_production)
                $("document").ready(function () {
                    var dataProvider = []
                    var monthes = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                    self.target_production.target.forEach(function (e, i) {
                        var dataProvideritem = {}
                        dataProvideritem.month = monthes[i]
                        dataProvideritem.target = e
                        dataProvideritem.production = self.target_production.production[i]
                        dataProvideritem.color = "#EE7879"
                        dataProvider.push(dataProvideritem)
                    })
                    var dataProvider2 = []
                    var chart = AmCharts.makeChart("ambarchart2", {
                        "type": "serial",
                        "addClassNames": true,
                        "theme": "light",
                        "autoMargins": false,
                        "marginLeft": 30,
                        "marginRight": 8,
                        "marginTop": 10,
                        "marginBottom": 26,
                        "balloon": {
                            "adjustBorderColor": false,
                            "horizontalPadding": 10,
                            "verticalPadding": 8,
                            "color": "#ffffff"
                        },

                        "dataProvider": dataProvider,
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
                            "lineColor": "#44ABAA",
                            "useLineColorForBulletBorder": true,
                            "bulletBorderThickness": 3,
                            "fillAlphas": 0,
                            "lineAlpha": 1,
                            "title": "Target",
                            "valueField": "target",
                            "dashLengthField": "dashLengthLine"
                        }],
                        "categoryField": "month",
                        "categoryAxis": {
                            "gridPosition": "start",
                            "axisAlpha": 0,
                            "tickLength": 0
                        },
                        "export": {
                            "enabled": false
                        }
                    });
                    console.log(self.production_compare)
                    self.production_compare.current_year.forEach(function (e, i) {
                        var dataProvideritem = {}
                        dataProvideritem.month = monthes[i]
                        dataProvideritem.current_year = e
                        dataProvideritem.last_year = self.production_compare.last_year[i]
                        dataProvideritem.color = "#bfbffd"
                        dataProvideritem.color2 = "#7474F0"
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
                    console.log(dataProvider2)

                })
            })


            return this._super().then(function () { })
        },
        fetch_data: function () {

            var user = session.uid
            var self = this;
            var get_production = rpc.query({
                model: "arope.broker",
                method: "get_production",
                args: [user]
            }).then(function (res) {
                self.brokerProduction = res
            })
            var get_rank = rpc.query({
                model: "arope.broker",
                method: "get_rank",
                args: [user]
            }).then(function (res) {
                self.brokerRank = res + 1
            });
            var get_target_production = rpc.query({
                model: "arope.broker",
                method: "get_target_production",
                args: [user]
            }).then(function (res) {
                self.target_production = res
            });
            var get_production_compare = rpc.query({
                model: "arope.broker",
                method: "get_production_compare",
                args: [user]
            }).then(function (res) {
                self.production_compare = res
            });
            return $.when(get_rank, get_production, get_target_production, get_production_compare);
        },
        makeNumber: function (x) {
            return parseFloat(x).toFixed(2).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")
        },


    });


    core.action_registry.add('hr_dashboard', HrDashboard);

    return HrDashboard;

});