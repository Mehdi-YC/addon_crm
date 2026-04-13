from odoo import models, fields, api
from odoo.exceptions import UserError


class CrmSendMailWizard(models.TransientModel):
    _name = "crm.send.mail.wizard"
    _description = "Send Mail to Store"

    store_id = fields.Many2one("crm_store", string="Store", required=True)
    subject = fields.Char(string="Subject", required=True)
    body = fields.Html(string="Message", required=True)
    email_to = fields.Char(string="Email Address")

    @api.onchange('store_id')
    def _onchange_store(self):
        """Auto-populate email from store contact if available"""
        if self.store_id and self.store_id.website:
            self.email_to = self.store_id.website

    def action_send_mail(self):
        """Send email to the store"""
        if not self.email_to or '@' not in self.email_to:
            raise UserError("Please provide a valid email address")
        
        # Update mail_sent flag
        self.store_id.mail_sent = True
        
        # Create email in Odoo mail system
        mail_values = {
            'subject': self.subject,
            'body': self.body,
            'email_to': self.email_to,
            'email_from': f"{self.env.user.name} <{self.env.user.email}>",
        }
        self.env['mail.mail'].create(mail_values).send()
        
        return {'type': 'ir.actions.act_window_close'}
