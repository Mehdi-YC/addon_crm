from . import models
from . import wizard


def post_init_hook(env):
    """Runs once after first install. Backfills source field."""
    leads = env['crm.lead'].search([('source', '=', False)])
    leads.write({'source': 'manual'})
