# -*- coding: utf-8 -*-
{
    'name': "pos_rating",
    'summary': "Short (1 phrase/line) summary of the module's purpose",
    'description': """
Long description of module's purpose
    """,
    'author': "Surya",
    'website': "https://www.yourcompany.com",
    'category': 'Point of Sale',
    'version': '0.1',
    'depends': ['base','point_of_sale'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/product_view.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_rating/static/src/js/pos_store.js',
            'pos_rating/static/src/js/pos_reciept.js',
            'pos_rating/static/src/css/pos_show_rating.css',
            'pos_rating/static/src/xml/pos_screen.xml',
            'pos_rating/static/src/xml/pos_reciept.xml',
        ],
    },
    'installable': True,
}

