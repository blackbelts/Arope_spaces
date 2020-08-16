# -*- coding: utf-8 -*-
{
    'name': "Arope Space",
    'summary': """Arope Space""",
    'description': """Spaces """,
    'author': "Black Belts Egypt",
    'website': "www.blackbelts-egypt.com",
    'category': 'arope',
    'version': '0.1',
    'license': 'AGPL-3',
    # any module necessary for this one to work correctly
    'depends': ['base','sales_team'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/setup.xml',
        'views/policy_view.xml',
        'views/collection.xml',
        'views/partner.xml',
        'views/get_a_quote.xml',
        'views/price_setup.xml',
        'views/targets.xml',
	    'views/dashboard_views.xml',
        # 'views/selection_question.xml',
        'views/medical_price_setup.xml',
        'views/insurance_application.xml',
        'views/actions.xml',
        'views/policy_num_wizard.xml',
        'views/state.xml',
        'views/menu_item.xml',

    ],
    'qweb': ["static/src/xml/hrms_dashboard.xml"],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
        # '/travel_quotation/static/src/css/main.css'
    ],
    'images': ['static/description/icon.png'],
    'css': ['static/src/css/main.css'],
}
