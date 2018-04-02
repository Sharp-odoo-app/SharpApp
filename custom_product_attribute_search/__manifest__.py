# -*- coding: utf-8 -*-
{
    'name': "Product Attribute Based Search",

    'summary': """
        Generate Name with Varient and Search by Varient """,

    'description': """
        roduct Attribute Based Search with varients
    """,

    'author': "Sharp IT",
    'website': "www.sharp4it.com",
    'price': 40.00, 
    'currency': 'EUR',     
    


    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['sale','product'],

    # always loaded
    'data': [],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'application': True,
}
