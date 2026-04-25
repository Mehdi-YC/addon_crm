import logging
from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class MyLeadCategory(models.Model):
    _name        = 'my.lead.category'
    _description = 'Lead Category'
    _order       = 'name'

    name   = fields.Char(required=True)
    code   = fields.Char(required=True)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'Category code must be unique.'),
    ]


class MyLeadInterest(models.Model):
    _name        = 'my.lead.interest'
    _description = 'Interest Tag'

    name = fields.Char(required=True)


class MyLeadCall(models.Model):
    _name        = 'my.lead.call'
    _description = 'Call Log'
    _order       = 'date desc'

    lead_id  = fields.Many2one('my.lead', ondelete='cascade', required=True)
    date     = fields.Datetime(default=fields.Datetime.now, required=True)
    duration = fields.Float(string='Duration (min)')
    answered = fields.Boolean()
    response = fields.Text(string='Notes / Response')


class MyLead(models.Model):
    _name        = 'my.lead'
    _description = 'Lead'
    _inherit     = ['mail.thread', 'mail.activity.mixin']
    _order       = 'create_date desc'
    _rec_name    = 'name'

    # ── Identity ──────────────────────────────────────────────────────────────
    name       = fields.Char(required=True, tracking=True)
    ref        = fields.Char(string='Reference', readonly=True, copy=False, default='New')
    partner_id = fields.Many2one('res.partner', string='Customer', tracking=True)
    user_id    = fields.Many2one('res.users', string='Salesperson',
                                 default=lambda self: self.env.user, tracking=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company)

    # ── Contact info ──────────────────────────────────────────────────────────
    phone   = fields.Char()
    email   = fields.Char()
    website = fields.Char()

    # ── Classification ────────────────────────────────────────────────────────
    category_id = fields.Many2one('my.lead.category', string='Category')
    source      = fields.Selection([
        ('api',      'API Import'),
        ('manual',   'Manual'),
        ('referral', 'Referral'),
        ('website',  'Website'),
    ], default='manual', tracking=True)

    # ── Pipeline ──────────────────────────────────────────────────────────────
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
    call_ids       = fields.One2many('my.lead.call', 'lead_id', string='Calls')
    call_count     = fields.Integer(compute='_compute_call_count', store=True)
    answered_count = fields.Integer(compute='_compute_call_count', store=True)

    # ── Interests tab ─────────────────────────────────────────────────────────
    interest_ids   = fields.Many2many('my.lead.interest', string='Interests',
                                      relation='my_lead_interest_rel',
                                      column1='lead_id', column2='interest_id')
    interest_notes = fields.Text(string='Interest Notes')

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

    # ── Constraints ───────────────────────────────────────────────────────────
    @api.constrains('expected_revenue')
    def _check_revenue(self):
        for rec in self:
            if rec.expected_revenue < 0:
                raise ValidationError('Expected revenue cannot be negative.')

    # ── CRUD ──────────────────────────────────────────────────────────────────
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('ref', 'New') == 'New':
                vals['ref'] = self.env['ir.sequence'].next_by_code('my.lead') or 'New'
        return super().create(vals_list)

    def unlink(self):
        if self.filtered(lambda r: r.state == 'won'):
            raise UserError('Cannot delete Won leads. Archive them instead.')
        return super().unlink()

    # ── State transitions ─────────────────────────────────────────────────────
    def action_qualify(self):
        self.write({'state': 'qualified'})

    def action_won(self):
        self.write({'state': 'won'})

    def action_lost(self):
        self.write({'state': 'lost'})

    def action_reset_new(self):
        self.filtered(lambda r: r.state == 'lost').write({'state': 'new'})

    # ── Bulk server action ────────────────────────────────────────────────────
    def action_bulk_qualify(self):
        to_qualify = self.filtered(lambda r: r.state == 'new')
        if not to_qualify:
            raise UserError('No new leads selected.')
        to_qualify.write({'state': 'qualified'})

    # ── Activity helper ───────────────────────────────────────────────────────
    def action_schedule_call(self):
        self.ensure_one()
        activity_type = self.env.ref('mail.mail_activity_data_call')
        self.activity_schedule(
            activity_type_id=activity_type.id,
            summary='Follow-up call',
            date_deadline=fields.Date.today() + timedelta(days=2),
            user_id=self.user_id.id or self.env.uid,
        )
