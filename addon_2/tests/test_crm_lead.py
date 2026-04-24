from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install', 'crm_custom')
class TestCrmLead(TransactionCase):
    """Unit tests for crm.lead model."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category = cls.env['crm.lead.category'].create({
            'name': 'Test Category',
            'code': 'test',
        })

    def setUp(self):
        super().setUp()
        self.lead = self.env['crm.lead'].create({
            'name':        'Test Lead',
            'category_id': self.category.id,
        })

    def test_initial_state(self):
        self.assertEqual(self.lead.state, 'new')
        self.assertEqual(self.lead.source, 'manual')
        self.assertNotEqual(self.lead.ref, 'New', 'Sequence should be assigned')

    def test_qualify(self):
        self.lead.action_qualify()
        self.assertEqual(self.lead.state, 'qualified')

    def test_won(self):
        self.lead.action_qualify()
        self.lead.action_won()
        self.assertEqual(self.lead.state, 'won')

    def test_negative_revenue_raises(self):
        from odoo.exceptions import ValidationError
        with self.assertRaises(ValidationError):
            self.lead.write({'expected_revenue': -100})

    def test_cannot_delete_won_lead(self):
        from odoo.exceptions import UserError
        self.lead.write({'state': 'won'})
        with self.assertRaises(UserError):
            self.lead.unlink()

    def test_call_count(self):
        self.env['crm.lead.call'].create({
            'lead_id':  self.lead.id,
            'answered': True,
        })
        self.env['crm.lead.call'].create({
            'lead_id':  self.lead.id,
            'answered': False,
        })
        self.lead.invalidate_recordset()
        self.assertEqual(self.lead.call_count, 2)
        self.assertEqual(self.lead.answered_count, 1)

    def test_bulk_qualify(self):
        leads = self.env['crm.lead'].create([
            {'name': f'Bulk Lead {i}', 'category_id': self.category.id}
            for i in range(3)
        ])
        leads.action_bulk_qualify()
        self.assertTrue(all(l.state == 'qualified' for l in leads))

    def test_onchange_partner_fills_phone(self):
        partner = self.env['res.partner'].create({
            'name':  'Test Partner',
            'phone': '0550001234',
            'email': 'test@example.com',
        })
        # Simulate onchange
        self.lead.partner_id = partner
        self.lead._onchange_partner()
        self.assertEqual(self.lead.phone, '0550001234')
        self.assertEqual(self.lead.email, 'test@example.com')


@tagged('post_install', '-at_install', 'crm_custom')
class TestImportWizard(TransactionCase):
    """Unit tests for the import wizard."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category = cls.env['crm.lead.category'].create({
            'name': 'Technology',
            'code': 'tech',
        })

    def test_wizard_fetches_preview(self):
        wizard = self.env['crm.import.wizard'].create({
            'category_id': self.category.id,
        })
        wizard._onchange_category()
        self.assertGreater(len(wizard.preview_ids), 0)

    def test_wizard_imports_leads(self):
        wizard = self.env['crm.import.wizard'].create({
            'category_id': self.category.id,
        })
        wizard._onchange_category()
        count_before = self.env['crm.lead'].search_count([])
        wizard.action_import()
        count_after = self.env['crm.lead'].search_count([])
        self.assertGreater(count_after, count_before)

    def test_wizard_empty_raises(self):
        from odoo.exceptions import UserError
        wizard = self.env['crm.import.wizard'].create({
            'category_id': self.category.id,
        })
        # Don't call onchange — preview_ids is empty
        with self.assertRaises(UserError):
            wizard.action_import()
