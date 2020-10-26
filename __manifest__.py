# -*- coding: utf-8 -*-
{
    'name': "Arope Space",
    'summary': """Arope Space""",
    'description': """Spaces """,
    'author': "Black Belts Egypt",
    'website': "www.blackbelts-egypt.com",
    'category': 'space',
    'version': '0.1',
    'license': 'AGPL-3',
    # any module necessary for this one to work correctly

    'depends': ['base','sales_team','helpdesk_inherit',
                'smart_travel_agency','personal_acciedent',
                'survey',
               'motor','medical' , 'mail','arope-conf'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/setup.xml',

        'views/get_a_quote.xml',
        'views/price_setup.xml',
        'views/targets.xml',
	    'views/dashboard_views.xml',
        'views/newdashboard.xml',
        'views/customer_dashboard_view.xml',
        'views/broker_dashboard_view.xml',
        'views/surveyor_dashboard_view.xml',
        'views/sub_questionnaire.xml',
        # 'views/medical_price_setup.xml',
        'views/insurance_application.xml',
        'views/actions.xml',
        'views/partner.xml',

        'views/policy_num_wizard.xml',
        'views/state.xml',
        'views/answer.xml',
        'views/claim_app.xml',
        'views/survey_setup.xml',
        'views/required_document_wizard.xml',
        'views/help_desk.xml',
        'views/policy_view.xml',
        #'reports/offer.xml',
        #'reports/questionnaire.xml',
        'views/menu_item.xml',


    ],
    'qweb': [
        "static/src/xml/hrms_dashboard.xml",
        "static/src/xml/new_dashboard.xml",
        "static/src/xml/broker_dash2.xml",
        "static/src/xml/surveyor_dash.xml",
        "static/src/xml/customer_dash.xml"
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
        # '/travel_quotation/static/src/css/main.css'
    ],
    'images': ['static/description/icon.png'],
    'css': ['/Arope-space/static/src/css/main.css'],
}
