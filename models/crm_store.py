from odoo import models, fields, api
import random
from datetime import date, timedelta
import base64
import csv
import io


class CrmStore(models.Model):
    _name = "crm_store"
    _description = "Store CRM"

    # MAIN
    store_id = fields.Char("Store ID", required=True)
    slug = fields.Char("Slug")
    name = fields.Char("Store Name")
    is_official = fields.Boolean("Official")
    announcement_id = fields.Char("Announcement ID")

    website = fields.Char("Website")
    phone = fields.Char("Phone")
    image_url = fields.Char("Logo")

    has_whatsapp = fields.Boolean("WhatsApp")
    has_viber = fields.Boolean("Viber")
    has_telegram = fields.Boolean("Telegram")

    # CALLS
    call1_answered = fields.Boolean()
    call1_date = fields.Date()
    call1_observation = fields.Text()

    call2_answered = fields.Boolean()
    call2_date = fields.Date()
    call2_observation = fields.Text()

    call3_answered = fields.Boolean()
    call3_date = fields.Date()
    call3_observation = fields.Text()

    # FINAL
    accepted = fields.Boolean()
    mail_sent = fields.Boolean()
    final_observation = fields.Text()

    # 🎯 RANDOM DATA GENERATOR
    def action_generate_random(self, count=20):
        for i in range(count):
            self.create({
                "store_id": str(random.randint(100000, 999999)),
                "slug": f"store-{i}",
                "name": f"Store {i}",
                "is_official": random.choice([True, False]),
                "announcement_id": str(random.randint(1000, 9999)),
                "website": f"https://store{i}.com",
                "phone": f"+2135{random.randint(10000000,99999999)}",
                "image_url": "https://via.placeholder.com/150",

                "has_whatsapp": random.choice([True, False]),
                "has_viber": random.choice([True, False]),
                "has_telegram": random.choice([True, False]),

                "call1_answered": random.choice([True, False]),
                "call1_date": date.today() - timedelta(days=random.randint(1, 10)),
                "call1_observation": "First call notes",

                "call2_answered": random.choice([True, False]),
                "call2_date": date.today() - timedelta(days=random.randint(1, 10)),
                "call2_observation": "Second call notes",

                "call3_answered": random.choice([True, False]),
                "call3_date": date.today() - timedelta(days=random.randint(1, 10)),
                "call3_observation": "Third call notes",

                "accepted": random.choice([True, False]),
                "mail_sent": random.choice([True, False]),
                "final_observation": "Final decision",
            })

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

    def action_mark_accepted(self):
        """Mark store as accepted"""
        self.accepted = True
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success',
                'message': f'{self.name} marked as accepted',
                'type': 'success',
                'sticky': False,
            }
        }

    def action_mark_rejected(self):
        """Mark store as rejected"""
        self.accepted = False
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success',
                'message': f'{self.name} marked as rejected',
                'type': 'warning',
                'sticky': False,
            }
        }

    def export_to_csv(self):
        """Export selected stores to CSV"""
        stores = self.search([])
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=[
            'store_id', 'name', 'slug', 'is_official', 'announcement_id',
            'website', 'phone', 'image_url', 'has_whatsapp', 'has_viber',
            'has_telegram', 'accepted', 'mail_sent'
        ])
        writer.writeheader()
        for store in stores:
            writer.writerow({
                'store_id': store.store_id,
                'name': store.name,
                'slug': store.slug,
                'is_official': store.is_official,
                'announcement_id': store.announcement_id,
                'website': store.website,
                'phone': store.phone,
                'image_url': store.image_url,
                'has_whatsapp': store.has_whatsapp,
                'has_viber': store.has_viber,
                'has_telegram': store.has_telegram,
                'accepted': store.accepted,
                'mail_sent': store.mail_sent,
            })
        return output.getvalue()
