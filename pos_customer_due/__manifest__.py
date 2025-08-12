# -*- coding: utf-8 -*-
{
    'name': "pos_customer_due",
    'summary': "Short (1 phrase/line) summary of the module's purpose",
    'description': """
Long description of module's purpose
    """,
    'author': "My Company",
    'website': "https://www.yourcompany.com",
    'category': 'Sales',
    'version': '0.1',
    'depends': ['base','point_of_sale'],
    'data': [
        'security/ir.model.access.csv',

        'views/pos_payment_method_form.xml',
        'views/res_partner_view.xml',
    ],
    'assets': {
            'point_of_sale._assets_pos': [
                'pos_customer_due/static/src/js/payment_screen.js',
            ],
        },
    'installable':True,
}

