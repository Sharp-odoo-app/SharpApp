{
    'name': 'PriceList Security',
    'version': '1.0',
    'author': 'Sharp IT',
    'website': 'www.sharp4it.com',
    'price': 20.00, 
    'category': 'Sales',
    'summary': '',
    'description': """
PriceList Security
================
It creates a many2many field between PriceLists and users. If you set Pricelists to User, then this PriceLists will be only seen by selected users.
This fields are only seen by users with "access right management"
    """,
    'images': [
    ],
    'depends': [
        'base',
        'product',
    ],
    'data': [
            'res_users_view.xml',
            'pricelist_view.xml',
            'security/pricelist_security_security.xml',
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
