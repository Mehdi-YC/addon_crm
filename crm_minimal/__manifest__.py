{
    'name': 'CRM Minimal',
    'version': '19.0.1.0.0',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/crm_data.xml',
        'views/crm_lead_views.xml',
        'wizard/bulk_create_wizard_views.xml',
    ],
    'installable': True,
    'application': True,
}
