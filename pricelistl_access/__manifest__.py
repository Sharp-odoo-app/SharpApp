{
    'name': 'PriceList access',
    'version': '0.1',
    'author': 'Sharp IT',
    'website': 'www.sharp4it.com',
    'price': 20.00,
    'currency': 'EUR',     
    'category': 'Sales',
    'summary': '',
    'description': """
it is managment users who can access to pricelist and which pricelist can be show to each user"
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
    'application': False,
}
