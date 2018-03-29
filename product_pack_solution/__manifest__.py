# -*- coding: utf-8 -*-
{
    'name': 'Product Pack Solution',
    'version': '1.0',
    'author': 'Sharp IT',
    'website': 'www.sharp4it.com',
    'category': 'Sales',
    'description': '''
    Create a products with pack and pass it to sale order, make sale order line
    like a bill of quantity, user can edit or add items from pack line page and
    group every product quantity and price then write all data to sale order line.  
    ''',
    'depends': ['sale'],
    'data': [
        'security/ir.model.access.csv',
        'security/view_section.xml',
        'views/product.xml',
        'views/sale_order.xml',
        'report/pack_offer_report.xml',
    ],
    'application': True,
}
