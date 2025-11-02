{
    'name': "Estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "lengocbao",
    'category': 'Category',
    'description': """
    Description text
    """,
    'data': [
        'data/ir.model.access.csv',
        'views/estate_users_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_views.xml',
        'reports/estate_property_reports.xml',
        'reports/estate_property_reports_templates.xml',
        'reports/inherit_estate_property_reports_templates.xml',
        'views/estate_menus.xml',
    ],
    'installable': True,
    'application': True,
}
