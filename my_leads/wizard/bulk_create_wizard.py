import random
from odoo import fields, models

_FIRST = ['Alpha', 'Beta', 'Gamma', 'Delta', 'Sigma', 'Nova', 'Apex', 'Zeta']
_LAST  = ['Corp', 'Tech', 'Group', 'Lab', 'Hub', 'Works', 'Systems', 'DZ']
_PHONE = ['055', '066', '077', '070', '033']


class MyLeadBulkWizard(models.TransientModel):
    _name        = 'my.lead.bulk.wizard'
    _description = 'Bulk Create Leads'

    keyword = fields.Char(string='Keyword', required=True,
                          help='Both generated lead names will include this word.')

    def action_create(self):
        leads = []
        for _ in range(2):
            first   = random.choice(_FIRST)
            last    = random.choice(_LAST)
            phone   = random.choice(_PHONE) + str(random.randint(1000000, 9999999))
            leads.append({
                'name':  f'{self.keyword} — {first} {last}',
                'phone': phone,
                'email': f'{first.lower()}.{last.lower()}@example.com',
            })

        created = self.env['my.lead'].create(leads)

        return {
            'type':      'ir.actions.act_window',
            'name':      'New Leads',
            'res_model': 'my.lead',
            'view_mode': 'list,form',
            'domain':    [('id', 'in', created.ids)],
            'target':    'current',
        }
