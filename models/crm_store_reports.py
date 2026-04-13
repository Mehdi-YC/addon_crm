from odoo import models, fields


class CrmStoreReportAcceptance(models.Model):
    _name = "crm.store.report.acceptance"
    _description = "Store Acceptance Report"
    _auto = False
    _order = 'name'

    name = fields.Char(string="Store Name")
    store_id = fields.Char(string="Store ID")
    accepted = fields.Boolean(string="Accepted")
    mail_sent = fields.Boolean(string="Mail Sent")
    is_official = fields.Boolean(string="Official")
    call_count = fields.Integer(string="Calls Logged")

    def init(self):
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW crm_store_report_acceptance AS (
                SELECT
                    cs.id,
                    cs.name,
                    cs.store_id,
                    cs.accepted,
                    cs.mail_sent,
                    cs.is_official,
                    CASE
                        WHEN cs.call1_answered THEN 1 ELSE 0
                    END +
                    CASE
                        WHEN cs.call2_answered THEN 1 ELSE 0
                    END +
                    CASE
                        WHEN cs.call3_answered THEN 1 ELSE 0
                    END as call_count
                FROM crm_store cs
            )
        """)


class CrmStoreReportCalls(models.Model):
    _name = "crm.store.report.calls"
    _description = "Store Call Statistics Report"
    _auto = False
    _order = 'name'

    name = fields.Char(string="Store Name")
    store_id = fields.Char(string="Store ID")
    call1_answered = fields.Boolean(string="Call 1 Answered")
    call2_answered = fields.Boolean(string="Call 2 Answered")
    call3_answered = fields.Boolean(string="Call 3 Answered")
    total_calls_answered = fields.Integer(string="Total Calls Answered")

    def init(self):
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW crm_store_report_calls AS (
                SELECT
                    cs.id,
                    cs.name,
                    cs.store_id,
                    cs.call1_answered,
                    cs.call2_answered,
                    cs.call3_answered,
                    CASE
                        WHEN cs.call1_answered THEN 1 ELSE 0
                    END +
                    CASE
                        WHEN cs.call2_answered THEN 1 ELSE 0
                    END +
                    CASE
                        WHEN cs.call3_answered THEN 1 ELSE 0
                    END as total_calls_answered
                FROM crm_store cs
            )
        """)
