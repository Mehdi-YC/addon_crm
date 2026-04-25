{
    'name': 'My Leads',
    'version': '19.0.1.0.0',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/my_leads_data.xml',
        'views/my_lead_views.xml',
        'wizard/bulk_create_views.xml',
    ],
    'installable': True,
    'application': True,
}
