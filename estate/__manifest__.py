{
    'name': "estate",
    'version': "1.0",
    'license': "AGPL-3",
    'depends': ['base'],
    'author': "sndibwami@virunga.org",
    'summary': "Real Estate Management",
    'application': True,
    'installable': True,
    'data': [
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menu.xml',
    ]
}
