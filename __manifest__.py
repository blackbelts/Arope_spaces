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

    'depends': ['base','sales_team','helpdesk_inherit',
                'smart_travel_agency','personal_acciedent',
<<<<<<< HEAD
               'motor','medical' , 'mail'],
=======
               'motor','medical' , 'mail','arope-conf'],
>>>>>>> 1aa7a965a46b9ba2a4e2f92ba6048b54f5e5e28a

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/setup.xml',
<<<<<<< HEAD
        'views/policy_view.xml',
        'views/collection.xml',
        'views/partner.xml',
        'views/get_a_quote.xml',
        'views/price_setup.xml',
=======
        'views/get_a_quote.xml',
        # 'views/price_setup.xml',
>>>>>>> 1aa7a965a46b9ba2a4e2f92ba6048b54f5e5e28a
        'views/targets.xml',
	    'views/dashboard_views.xml',
        'views/sub_questionnaire.xml',
        # 'views/medical_price_setup.xml',
        'views/insurance_application.xml',
        'views/actions.xml',
<<<<<<< HEAD
        'views/claim.xml',
=======
>>>>>>> 1aa7a965a46b9ba2a4e2f92ba6048b54f5e5e28a
        'views/policy_num_wizard.xml',
        'views/state.xml',
        'views/answer.xml',
        'views/claim_app.xml',
        # 'views/help_desk.xml',
        #'reports/offer.xml',
        #'reports/questionnaire.xml',
        'views/menu_item.xml',
<<<<<<< HEAD
        'wizard/users.xml',
=======
>>>>>>> 1aa7a965a46b9ba2a4e2f92ba6048b54f5e5e28a

    ],
    'qweb': ["static/src/xml/hrms_dashboard.xml"],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
        # '/travel_quotation/static/src/css/main.css'
    ],
    'images': ['static/description/icon.png'],
    'css': ['/Arope-space/static/src/css/main.css'],
}
