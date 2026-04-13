from odoo import models, fields, api
from datetime import date


class CrmCallLogWizard(models.TransientModel):
    _name = "crm.call.log.wizard"
    _description = "Log Call for Store"

    store_id = fields.Many2one("crm_store", string="Store", required=True)
    call_number = fields.Selection([
        ('1', 'Call 1'),
        ('2', 'Call 2'),
        ('3', 'Call 3'),
    ], string="Call Number", required=True, default='1')
    answered = fields.Boolean(string="Call Answered", default=False)
    call_date = fields.Date(string="Call Date", default=date.today, required=True)
    observation = fields.Text(string="Observation", required=True)

    def action_log_call(self):
        """Log the call for the selected store"""
        if self.call_number == '1':
            self.store_id.write({
                'call1_answered': self.answered,
                'call1_date': self.call_date,
                'call1_observation': self.observation,
            })
        elif self.call_number == '2':
            self.store_id.write({
                'call2_answered': self.answered,
                'call2_date': self.call_date,
                'call2_observation': self.observation,
            })
        elif self.call_number == '3':
            self.store_id.write({
                'call3_answered': self.answered,
                'call3_date': self.call_date,
                'call3_observation': self.observation,
            })
        return {'type': 'ir.actions.act_window_close'}
