# -*- coding: utf-8 -*-
{
    'name' :'Component Request',
    'version' : '18.0',
    'depends' : ['base','sale','purchase','stock'],
    'author' : 'Surya',
    'category': 'Component Request/Component Request',
    'description' : """""",
    'data': [
        'security/res_groups.xml',
        'security/ir.model.access.csv',

        'data/ir_sequence_data.xml',

        'views/component_request_views.xml',
        'views/purchase_order_views.xml',
        'views/stock_picking_views.xml',
        'views/component_request_menu.xml'
    ],
    'sequence':"2",
    'application':True,
    'installable':True,
    'license': 'LGPL-3'
}