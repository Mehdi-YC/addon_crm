import logging
from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class CrmLeadCall(models.Model):
    """Log of phone calls made on a lead."""
    _name        = 'crm.lead.call'
    _description = 'Call Log'
    _order       = 'date desc'

    lead_id  = fields.Many2one('crm.lead', ondelete='cascade', required=True)
    date     = fields.Datetime(default=fields.Datetime.now, required=True)
    duration = fields.Float(string='Duration (min)')
    answered = fields.Boolean()
    response = fields.Text(string='Notes / Response')


class CrmLead(models.Model):
    _name        = 'crm.lead'
    _description = 'Lead'
    _inherit     = ['mail.thread', 'mail.activity.mixin']
    _order       = 'create_date desc'
    _rec_name    = 'name'

    # ── Identity ──────────────────────────────────────────────────────────────
    name       = fields.Char(required=True, tracking=True)
    ref        = fields.Char(
        string='Reference', readonly=True, copy=False, default='New',
        help='Auto-generated reference number.',
    )
    partner_id = fields.Many2one('res.partner', string='Customer', tracking=True)
    user_id    = fields.Many2one(
        'res.users', string='Salesperson',
        default=lambda self: self.env.user,
        tracking=True,
    )
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.company,
    )

    # ── Contact info ──────────────────────────────────────────────────────────
    phone   = fields.Char()
    email   = fields.Char()
    website = fields.Char()

    # ── Classification ────────────────────────────────────────────────────────
    category_id = fields.Many2one('crm.lead.category', string='Category')
    source      = fields.Selection([
        ('api',      'API Import'),
        ('manual',   'Manual'),
        ('referral', 'Referral'),
        ('website',  'Website'),
    ], default='manual', tracking=True)

    # ── Pipeline / State ──────────────────────────────────────────────────────
    state = fields.Selection([
        ('new',       'New'),
        ('qualified', 'Qualified'),
        ('proposal',  'Proposal Sent'),
        ('won',       'Won'),
        ('lost',      'Lost'),
    ], default='new', string='Status', tracking=True, index=True)

    expected_revenue = fields.Float(tracking=True)
    notes            = fields.Html(string='Internal Notes')

    # ── Calls tab ─────────────────────────────────────────────────────────────
    call_ids      = fields.One2many('crm.lead.call', 'lead_id', string='Calls')
    call_count    = fields.Integer(compute='_compute_call_count', store=True)
    answered_count = fields.Integer(compute='_compute_call_count', store=True)

    # ── Interests tab ─────────────────────────────────────────────────────────
    interest_ids   = fields.Many2many(
        'crm.lead.interest', string='Interests',
        relation='crm_lead_interest_rel',
        column1='lead_id', column2='interest_id',
    )
    interest_notes = fields.Text(string='Interest Notes')

    # ── SQL constraints ───────────────────────────────────────────────────────
    _sql_constraints = [
        ('ref_unique', 'UNIQUE(ref)', 'Reference must be unique.'),
    ]

    # ── Computed ──────────────────────────────────────────────────────────────
    @api.depends('call_ids', 'call_ids.answered')
    def _compute_call_count(self):
        for rec in self:
            rec.call_count     = len(rec.call_ids)
            rec.answered_count = len(rec.call_ids.filtered('answered'))

    # ── Onchange ──────────────────────────────────────────────────────────────
    @api.onchange('partner_id')
    def _onchange_partner(self):
        if self.partner_id:
            self.phone = self.partner_id.phone
            self.email = self.partner_id.email
            if not self.partner_id.email:
                return {'warning': {
                    'title':   'No email',
                    'message': 'This customer has no email address.',
                }}

    # ── Python constraints ────────────────────────────────────────────────────
    @api.constrains('expected_revenue')
    def _check_revenue(self):
        for rec in self:
            if rec.expected_revenue < 0:
                raise ValidationError('Expected revenue cannot be negative.')

    # ── CRUD overrides ────────────────────────────────────────────────────────
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('ref', 'New') == 'New':
                vals['ref'] = self.env['ir.sequence'].next_by_code('crm.lead') or 'New'
        return super().create(vals_list)

    def unlink(self):
        if self.filtered(lambda r: r.state == 'won'):
            raise UserError('Cannot delete Won leads. Archive them instead.')
        return super().unlink()

    # ── State transitions ─────────────────────────────────────────────────────
    def action_qualify(self):
        self.write({'state': 'qualified'})

    def action_send_proposal(self):
        self.write({'state': 'proposal'})

    def action_won(self):
        self.write({'state': 'won'})

    def action_lost(self):
        self.write({'state': 'lost'})

    def action_reset_new(self):
        self.filtered(lambda r: r.state == 'lost').write({'state': 'new'})

    # ── Bulk server action ────────────────────────────────────────────────────
    def action_bulk_qualify(self):
        """Server action: mark selected new leads as qualified."""
        to_qualify = self.filtered(lambda r: r.state == 'new')
        if not to_qualify:
            raise UserError('No new leads selected.')
        to_qualify.write({'state': 'qualified'})

    # ── Activity helpers ──────────────────────────────────────────────────────
    def action_schedule_call(self):
        """Schedule a follow-up call activity in 2 days."""
        self.ensure_one()
        activity_type = self.env.ref('mail.mail_activity_data_call')
        self.activity_schedule(
            activity_type_id=activity_type.id,
            summary='Follow-up call',
            date_deadline=fields.Date.today() + timedelta(days=2),
            user_id=self.user_id.id or self.env.uid,
        )

    # ── Cron ──────────────────────────────────────────────────────────────────
    @api.model
    def _cron_auto_qualify_leads(self):
        """Cron: auto-qualify leads with 3+ answered calls older than 7 days."""
        cutoff = fields.Datetime.now() - timedelta(days=7)
        leads = self.search([
            ('state', '=', 'new'),
            ('create_date', '<=', cutoff),
        ])
        qualified = self.env['crm.lead']
        for lead in leads:
            if lead.answered_count >= 3:
                qualified |= lead
        if qualified:
            qualified.with_context(mail_notrack=True).write({'state': 'qualified'})
            _logger.info('Auto-qualified %d leads', len(qualified))

    # ── Stats helper (raw SQL example) ───────────────────────────────────────
    @api.model
    def _get_revenue_by_category(self):
        """Return total revenue per category using raw SQL."""
        self.env.cr.execute("""
            SELECT
                c.name  AS category,
                COUNT(l.id) AS lead_count,
                COALESCE(SUM(l.expected_revenue), 0) AS total_revenue
            FROM crm_lead l
            LEFT JOIN crm_lead_category c ON c.id = l.category_id
            WHERE l.state NOT IN ('lost')
            GROUP BY c.name
            ORDER BY total_revenue DESC
        """)
        return self.env.cr.dictfetchall()
