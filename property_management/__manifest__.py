# -*- coding: utf-8 -*-
{
    'name': 'Property Management',
    'version': '1.0',
    'depends': ['base', 'mail', 'sale' , 'web' , 'website'],
    'author': "Surya",
    'category': 'Sales/Property',
    'description': """
    Module For Property Management
    """,
    'data': [
        'security/property_management_security.xml',
        'security/res_groups.xml',
        'security/ir.model.access.csv',

        'report/rental_lease_management_report.xml',
        'report/rental_lease_management_paper_format.xml',
        'report/ir_actions_report.xml',

        'data/property_data.xml',
        'data/mail_template_order.xml',
        'data/ir_cron_data.xml',
        'data/ir_sequence_data.xml',

        'wizard/rental_lease_management_make_report_views.xml',
        'views/res_partner_inherit_view.xml',
        'views/property_management_views.xml',
        'views/rental_lease_management_views.xml',
        'views/account_move_inherit_property_management.xml',
        'views/property_management_menu.xml',
        'views/property_management_template.xml',
        'views/property_management_home_template.xml',
        'views/snippets/latest_property_snippet.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'property_management/static/src/js/action_manager.js',
        ],
        'web.assets_frontend': [
            'property_management/static/src/xml/property_highlight_content.xml',
            'property_management/static/src/js/property_management_webpage.js',
            'property_management/static/src/js/latest_property_snippet.js',
        ],
    },
    'sequence': "1",
    'application': True,
    'installable': True,
    'license': 'LGPL-3'
}
