from odoo import api, fields, models
from odoo.exceptions import UserError


class ImportLeadsWizardLine(models.TransientModel):
    """A single lead preview row in the import wizard."""
    _name        = 'crm.import.wizard.line'
    _description = 'Import Wizard Line'

    wizard_id        = fields.Many2one('crm.import.wizard', ondelete='cascade')
    name             = fields.Char(string='Lead Name', required=True)
    phone            = fields.Char()
    email            = fields.Char()
    expected_revenue = fields.Float()


class ImportLeadsWizard(models.TransientModel):
    """Wizard: select a category → preview leads from API → import."""
    _name        = 'crm.import.wizard'
    _description = 'Import Leads from API'

    category_id  = fields.Many2one(
        'crm.lead.category', required=True, string='Category',
        help='Select a category to fetch leads from the external API.',
    )
    preview_ids  = fields.One2many(
        'crm.import.wizard.line', 'wizard_id', string='Leads Preview',
    )
    import_count = fields.Integer(
        compute='_compute_import_count', string='Leads to import',
    )

    # ── Computed ──────────────────────────────────────────────────────────────
    @api.depends('preview_ids')
    def _compute_import_count(self):
        for rec in self:
            rec.import_count = len(rec.preview_ids)

    # ── Onchange: fetch when category changes ─────────────────────────────────
    @api.onchange('category_id')
    def _onchange_category(self):
        if not self.category_id:
            self.preview_ids = [(5, 0, 0)]
            return
        data = self._fetch_from_api(self.category_id.code)
        self.preview_ids = [(5, 0, 0)]   # clear old lines
        self.preview_ids = [
            (0, 0, {
                'name':             lead['name'],
                'phone':            lead.get('phone', ''),
                'email':            lead.get('email', ''),
                'expected_revenue': lead.get('revenue', 0.0),
            })
            for lead in data
        ]

    # ── Mock API fetch ────────────────────────────────────────────────────────
    def _fetch_from_api(self, category_code):
        """
        Fetch leads from external API by category code.

        Replace the mock_data dict with a real HTTP call:

            import requests
            api_url = self.env['ir.config_parameter'].sudo().get_param(
                'crm_custom.api_url', 'https://api.example.com'
            )
            api_key = self.env['ir.config_parameter'].sudo().get_param(
                'crm_custom.api_key', ''
            )
            resp = requests.get(
                f'{api_url}/leads',
                params={'category': category_code},
                headers={'Authorization': f'Bearer {api_key}'},
                timeout=10,
            )
            resp.raise_for_status()
            return resp.json()
        """
        mock_data = {
            'tech': [
                {
                    'name':    'TechCorp DZ',
                    'phone':   '0550001111',
                    'email':   'info@techcorp.dz',
                    'revenue': 85000,
                },
                {
                    'name':    'Algiers AI Lab',
                    'phone':   '0661234567',
                    'email':   'hi@algiers.ai',
                    'revenue': 120000,
                },
                {
                    'name':    'Annaba Software',
                    'phone':   '0770987654',
                    'email':   'contact@annaba.dev',
                    'revenue': 55000,
                },
            ],
            'retail': [
                {
                    'name':    'Oran Retail Group',
                    'phone':   '0777654321',
                    'email':   'oran@retail.dz',
                    'revenue': 30000,
                },
                {
                    'name':    'Constantine Mall',
                    'phone':   '0555123456',
                    'email':   'info@constantine.dz',
                    'revenue': 45000,
                },
            ],
            'referral': [
                {
                    'name':    'Bejaia Partners',
                    'phone':   '0666789012',
                    'email':   'contact@bejaia.dz',
                    'revenue': 70000,
                },
            ],
        }
        return mock_data.get(category_code, [])

    # ── Import action ─────────────────────────────────────────────────────────
    def action_import(self):
        """Create crm.lead records from the preview lines."""
        self.ensure_one()
        if not self.preview_ids:
            raise UserError(
                'No leads to import. Please select a category first.'
            )

        Lead = self.env['crm.lead']
        created = Lead.create([
            {
                'name':             line.name,
                'phone':            line.phone,
                'email':            line.email,
                'expected_revenue': line.expected_revenue,
                'category_id':      self.category_id.id,
                'source':           'api',
            }
            for line in self.preview_ids
        ])

        # After import, open the newly created leads
        return {
            'type':      'ir.actions.act_window',
            'name':      f'Imported {len(created)} Lead(s)',
            'res_model': 'crm.lead',
            'view_mode': 'list,form',
            'domain':    [('id', 'in', created.ids)],
            'target':    'current',
        }
