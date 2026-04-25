import random
from odoo import fields, models


# Random data pools
_FIRST = ['Alpha', 'Beta', 'Gamma', 'Delta', 'Sigma', 'Nova', 'Apex', 'Zeta']
_LAST  = ['Corp', 'Tech', 'Group', 'Lab', 'Hub', 'Works', 'Systems', 'DZ']
_PHONE = ['055', '066', '077', '070', '033']


class BulkCreateWizard(models.TransientModel):
    _name        = 'crm.bulk.create.wizard'
    _description = 'Bulk Create Leads'

    keyword = fields.Char(string='Keyword', required=True,
                          help='The 2 generated lead names will include this word.')

    def action_create(self):
        leads = []
        for _ in range(2):
            first  = random.choice(_FIRST)
            last   = random.choice(_LAST)
            phone  = random.choice(_PHONE) + str(random.randint(1000000, 9999999))
            revenue = random.randint(1, 200) * 1000

            leads.append({
                'name':             f'{self.keyword} — {first} {last}',
                'phone':            phone,
                'email':            f'{first.lower()}.{last.lower()}@example.com',
                'expected_revenue': revenue,
            })

        created = self.env['crm.lead'].create(leads)

        # Close wizard and show the new records
        return {
            'type':      'ir.actions.act_window',
            'name':      'New Leads',
            'res_model': 'crm.lead',
            'view_mode': 'list,form',
            'domain':    [('id', 'in', created.ids)],
            'target':    'current',
        }
