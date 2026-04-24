from odoo import models, fields, api
import random
from datetime import date, timedelta


class CrmStore(models.Model):
    _name = "crm_store"
    _description = "Store CRM"

    # Basic Information
    store_id = fields.Char("Store ID", required=True)
    slug = fields.Char("Slug")
    name = fields.Char("Store Name")
    is_official = fields.Boolean("Official")
    announcement_id = fields.Char("Announcement ID")

    # Contact Information
    website = fields.Char("Website")
    phone = fields.Char("Phone")
    image_url = fields.Char("Logo")

    # Communication Channels
    has_whatsapp = fields.Boolean("WhatsApp")
    has_viber = fields.Boolean("Viber")
    has_telegram = fields.Boolean("Telegram")

    # Call History
    call1_answered = fields.Boolean("Call 1 Answered")
    call1_date = fields.Date("Call 1 Date")
    call1_observation = fields.Text("Call 1 Notes")

    call2_answered = fields.Boolean("Call 2 Answered")
    call2_date = fields.Date("Call 2 Date")
    call2_observation = fields.Text("Call 2 Notes")

    call3_answered = fields.Boolean("Call 3 Answered")
    call3_date = fields.Date("Call 3 Date")
    call3_observation = fields.Text("Call 3 Notes")

    # Final Decision
    accepted = fields.Boolean("Accepted")
    mail_sent = fields.Boolean("Mail Sent")
    final_observation = fields.Text("Final Notes")

    def action_log_call(self):
        """Open wizard to log a call"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Log Call',
            'res_model': 'crm.call.log.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_store_id': self.id},
        }

    def action_send_mail(self):
        """Open wizard to send mail"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Send Mail',
            'res_model': 'crm.send.mail.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_store_id': self.id},
        }
