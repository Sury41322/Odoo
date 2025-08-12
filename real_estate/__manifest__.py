{
    'name': 'Real Estate',
    'version': '1.0',
    'depends': ['base',
                'mail'],
    'author': "Surya",
    'category': 'Sales/College',
    'description': """
    Real Estate
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        # 'views/mymodule_view.xml',

        'views/estate_property_tags.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_views.xml',
        'views/estate_menu.xml'
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
        # 'demo/demo_data.xml',
    ],
    'sequence':"1",
    'application':True,
    'installable':True,
    'license': 'LGPL-3',
}