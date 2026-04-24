from odoo import models, fields, api
from odoo.exceptions import UserError
import csv
import io
import base64


class CrmBulkImportWizard(models.TransientModel):
    _name = "crm.bulk.import.wizard"
    _description = "Bulk Import Stores"

    import_file = fields.Binary(string="Import File (CSV)", required=True)
    file_name = fields.Char(string="File Name")
    import_type = fields.Selection([
        ('create', 'Create New Stores'),
        ('update', 'Update Existing Stores'),
    ], string="Import Type", default='create', required=True)
    skip_errors = fields.Boolean(string="Skip Errors", default=True)

    def action_import(self):
        """Import stores from CSV file"""
        if not self.import_file:
            raise UserError("Please select a file to import")
        
        try:
            # Decode file
            file_data = base64.b64decode(self.import_file)
            file_str = file_data.decode('utf-8')
            
            # Parse CSV
            csv_reader = csv.DictReader(io.StringIO(file_str))
            imported = 0
            errors = []
            
            for row in csv_reader:
                try:
                    if self.import_type == 'create':
                        self.env['crm_store'].create({
                            'store_id': row.get('store_id', ''),
                            'name': row.get('name', ''),
                            'slug': row.get('slug', ''),
                            'is_official': row.get('is_official', '').lower() in ['true', '1', 'yes'],
                            'announcement_id': row.get('announcement_id', ''),
                            'website': row.get('website', ''),
                            'phone': row.get('phone', ''),
                            'image_url': row.get('image_url', ''),
                            'has_whatsapp': row.get('has_whatsapp', '').lower() in ['true', '1', 'yes'],
                            'has_viber': row.get('has_viber', '').lower() in ['true', '1', 'yes'],
                            'has_telegram': row.get('has_telegram', '').lower() in ['true', '1', 'yes'],
                        })
                        imported += 1
                    elif self.import_type == 'update':
                        store = self.env['crm_store'].search([('store_id', '=', row.get('store_id'))])
                        if store:
                            store.write({
                                'name': row.get('name', store.name),
                                'website': row.get('website', store.website),
                                'phone': row.get('phone', store.phone),
                            })
                            imported += 1
                except Exception as e:
                    if self.skip_errors:
                        errors.append(f"Row skipped: {str(e)}")
                    else:
                        raise UserError(f"Import failed: {str(e)}")
            
            message = f"Successfully imported {imported} stores"
            if errors:
                message += f"\nErrors: {len(errors)} skipped"
            
            return {
                'effect': {
                    'fadeout': True,
                    'type': 'rainbow_man',
                    'message': message,
                }
            }
        
        except Exception as e:
            raise UserError(f"Error reading file: {str(e)}")
