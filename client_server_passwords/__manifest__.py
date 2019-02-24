# -*- coding: utf-8 -*-
#################################################################################
# Author      : SharpeIT Business Solutions (<www.sharp4IT.com>)                #
# Copyright(c): 2015-Present SharpeIT Business Solutions                        #
# All Rights Reserved.                                                          #
#                                                                               #
# This program is copyright property of the author mentioned above.             #
# You can`t redistribute it and/or modify it.                                   #
#                                                                               #
#################################################################################
{
    'name': "Client Server Passwords",

    'summary': """
        Add a table in customer page to save server and ips or url and username and password""",

    'description': """
        Add a table in customer page to save server and ips or url and username and password
    """,

    'author': "Sharp IT",
    'website': "http://www.sharp4it.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'sale',
    'version': '0.1',
    'price': '0.0',
    'currency': 'EUR',
    # any module necessary for this one to work correctly
    'depends': ['sale_management'],

    # always loaded
    'data': [
        'data/data.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'images': [
        'static/description/banner.png',
        'static/description/cover.png',
    ],
    'application': True,
}
