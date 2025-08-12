# -*- coding: utf-8 -*-
{
    'name': "payment_paytrial",
    'summary': "A payment provider for running fake payment flows for Paytrial purposes",
    'description': """
Long description of module's purpose
    """,
    'author': "My Company",
    'website': "https://www.yourcompany.com",
    'category': 'Hidden',
    'version': '0.1',
    'depends': ['payment'],
    'data': [
        # 'views/payment_paytrial_template.xml',
        # 'views/payment_provider_views.xml',
        # 'views/payment_token_views.xml',
        # 'views/payment_transaction_views.xml',

        'data/payment_method_data.xml',
        'data/payment_provider_data.xml',  # Depends on `payment_method_paytrial`.
    ],
    'assets': {
        'web.assets_frontend': [
            # 'payment_paytrial/static/src/js/**/*',
        ],
    },
    'license': 'LGPL-3',
}

