{
    'name': 'CRM Custom',
    'version': '19.0.1.0.0',
    'category': 'CRM',
    'summary': 'Custom CRM with API import wizard',
    'author': 'You',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/crm_security.xml',
        'data/crm_data.xml',
        'views/crm_lead_views.xml',
        'views/crm_lead_wizard.xml',
        'views/menus.xml',
    ],
    'post_init_hook': 'post_init_hook',
    'installable': True,
    'application': True,
}
