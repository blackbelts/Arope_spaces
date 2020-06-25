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
    'depends': ['base',],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        # 'security/security.xml',
        'views/setup.xml',
        'views/policy_view.xml',
        'views/collection.xml',
        'views/partner.xml',
        'views/menu_item.xml',


    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
