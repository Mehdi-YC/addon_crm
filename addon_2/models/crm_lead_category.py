from odoo import fields, models


class CrmLeadCategory(models.Model):
    _name        = 'crm.lead.category'
    _description = 'Lead Category'
    _order       = 'name'

    name   = fields.Char(required=True)
    code   = fields.Char(required=True, help='Used to identify the category in API calls.')
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'Category code must be unique.'),
    ]


class CrmLeadInterest(models.Model):
    _name        = 'crm.lead.interest'
    _description = 'Interest Tag'

    name = fields.Char(required=True)
