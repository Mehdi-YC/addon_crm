import random
from odoo import api, fields, models
from odoo.exceptions import UserError

_FIRST = ['Alpha', 'Beta', 'Gamma', 'Delta', 'Sigma', 'Nova', 'Apex', 'Zeta']
_LAST  = ['Corp', 'Tech', 'Group', 'Lab', 'Hub', 'Works', 'Systems', 'DZ']
_PHONE = ['055', '066', '077', '070', '033']


class MyLead(models.Model):
    _name        = 'my.lead'
    _description = 'Store Lead'
    _inherit     = ['mail.thread', 'mail.activity.mixin']
    _order       = 'create_date desc'
    _rec_name    = 'name'

    # ── Main Info ─────────────────────────────────────────────────────────────
    name            = fields.Char(string='Store Name', tracking=True)
    store_id        = fields.Char(string='Store ID (Ouedkniss)', readonly=True)
    slug            = fields.Char(string='Slug', readonly=True)
    is_official     = fields.Boolean(string='Official')
    announcement_id = fields.Char(string='Announcement ID', readonly=True)
    website         = fields.Char(string='Website')
    phone           = fields.Char(string='Phone')
    image_url       = fields.Char(string='Logo URL', readonly=True)
    has_whatsapp    = fields.Boolean(string='WhatsApp', readonly=True)
    has_viber       = fields.Boolean(string='Viber', readonly=True)
    has_telegram    = fields.Boolean(string='Telegram', readonly=True)

    # ── Pipeline state ────────────────────────────────────────────────────────
    state = fields.Selection([
        ('new',       'New'),
        ('qualified', 'Qualified'),
        ('proposal',  'Proposition'),
        ('won',       'Won'),
        ('lost',      'Lost'),
    ], default='new', string='Status', tracking=True, index=True)

    # ── Call 1 ────────────────────────────────────────────────────────────────
    call1_answered    = fields.Boolean(string='Answered?')
    call1_date        = fields.Date(string='Call Date')
    call1_observation = fields.Text(string='Observation')

    # ── Call 2 ────────────────────────────────────────────────────────────────
    call2_answered    = fields.Boolean(string='Answered?')
    call2_date        = fields.Date(string='Call Date')
    call2_observation = fields.Text(string='Observation')

    # ── Call 3 ────────────────────────────────────────────────────────────────
    call3_answered    = fields.Boolean(string='Answered?')
    call3_date        = fields.Date(string='Call Date')
    call3_observation = fields.Text(string='Observation')

    # ── Final ─────────────────────────────────────────────────────────────────
    accepted          = fields.Boolean(string='Accepted', tracking=True)
    mail_sent         = fields.Boolean(string='Mail Sent', tracking=True)
    final_observation = fields.Text(string='Final Observation')

    # ── State transitions ─────────────────────────────────────────────────────
    def action_qualify(self):
        self.write({'state': 'qualified'})

    def action_proposal(self):
        self.write({'state': 'proposal'})

    def action_won(self):
        self.write({'state': 'won'})

    def action_lost(self):
        self.write({'state': 'lost'})

    def action_reset(self):
        self.write({'state': 'new'})

    # ── Bulk create (server action from list view) ────────────────────────────
    def action_open_bulk_create(self):
        return {
            'type':      'ir.actions.act_window',
            'name':      'Bulk Create Leads',
            'res_model': 'my.lead.bulk.wizard',
            'view_mode': 'form',
            'target':    'new',
        }
