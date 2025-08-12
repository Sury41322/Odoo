{
    'name': "payment_paytrail_nets",
    'summary': "Short (1 phrase/line) summary of the module's purpose",
    'description': """
Long description of module's purpose
    """,
    'author': "My Company",
    'website': "https://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['payment','account'],
    'data': [
        'views/payment_paytrail_templates.xml',
        'views/payment_provider_view_form.xml',
        'data/payment_method_data.xml',
        'data/payment_provider_data.xml',
    ],
    'post_init_hook': 'post_install_hook',
    'uninstall_hook': 'uninstall_hook',
    'license': 'LGPL-3',
}
