# -*- coding: utf-8 -*-
# tutorial
{
    'name': "Real Estate",
    'version': '1.0',
    'license': 'AGPL-3',
    'depends': ['base'],
    'author': "aleon",
    'category': 'Test',
    'description': "Description of Real Estate",
    # data files always loaded at installation
    'data': [
        # data
        # views
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        # access
        'security/ir.model.access.csv',
    ],
    # data files containing optionally loaded demonstration data
    # 'demo': ['demo/demo_data.xml',],
}
