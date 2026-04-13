# CRM Store Module - Complete Documentation

## Overview
A complete Odoo module for managing store CRMs with call logging, email communication, acceptance tracking, and reporting.

## Features

### 1. **Store Management**
- Store ID, Name, and Slug tracking
- Official store designation
- Contact information (website, phone)
- Logo/image support
- Communication channel availability (WhatsApp, Viber, Telegram)

### 2. **Call Logging System**
- Track up to 3 calls per store
- Record call date, whether answered, and observations
- Quick call logging via wizard interface
- Call history view in form

### 3. **Email Communication**
- Send emails to stores directly from the system
- Email status tracking (mail_sent flag)
- HTML email support

### 4. **Bulk Import**
- Import stores from CSV files
- Create new stores or update existing ones
- Error tolerance with skip options
- Validation and feedback

### 5. **Store Acceptance Workflow**
- Track store acceptance status
- Final observations/notes
- One-click mark as accepted/rejected buttons

### 6. **Reports & Analytics**
- **Acceptance Status Report**: View acceptance rate and statistics
- **Call Statistics Report**: Track call response rates and patterns
- Pivot table and chart views
- Group by official status, acceptance, mail sent, and call dates

### 7. **Views**
- **List View**: Quick overview of all stores with key metrics
- **Form View**: Detailed store information with tabbed organization
- **Kanban View**: Visual board grouped by acceptance status
- **Search View**: Advanced filters and grouping options

## Menu Structure
```
Store CRM (Main Module)
├── Stores (Main action - list/form/kanban)
├── Import Stores (Bulk import wizard)
└── Reports
    ├── Acceptance Status
    └── Call Statistics
```

## How to Use

### Manage Stores
1. Go to **Store CRM** > **Stores**
2. Create a new store with required information
3. Fill in contact details and communication channels

### Log Calls
1. Open a store record
2. Click **Log Call** button
3. Select call number (1, 2, or 3)
4. Mark if answered and add observations
5. Click Save

### Send Emails
1. Open a store record
2. Click **Send Mail** button
3. Enter email address, subject, and message
4. Click Send Mail
5. Flag will update automatically

### Import Stores
1. Go to **Store CRM** > **Import Stores**
2. Select import type (Create New or Update Existing)
3. Select your CSV file
4. Click Import

### CSV Format for Bulk Import
```csv
store_id,name,slug,is_official,announcement_id,website,phone,image_url,has_whatsapp,has_viber,has_telegram
ST001,Store One,store-one,true,ANN001,https://store1.com,+1234567890,https://url.com/logo.png,true,false,true
ST002,Store Two,store-two,false,ANN002,https://store2.com,+1234567891,https://url.com/logo2.png,false,true,false
```

### View Reports
1. Go to **Store CRM** > **Reports** > **Acceptance Status** or **Call Statistics**
2. Use pivot view to analyze data
3. Group by different dimensions
4. View charts for visual representation

## Security

### User Groups
- **Store CRM User**: Read/Write access to all stores
- **Store CRM Admin**: Full access including delete

### Access Control
- Base group_user: Limited access
- System group: Full admin access

## Advanced Features

### Actions
- **Mark Accepted**: One-click to accept a store
- **Mark Rejected**: One-click to reject a store
- **Export CSV**: Export store data

### Filters
- Official Stores
- Accepted/Pending
- Mail Sent Status
- Call Response Status

### Grouping Options
- By Official Status
- By Acceptance Status
- By Mail Sent Status
- By Call Date

## Data Model

### crm_store
Main model containing all store information

**Key Fields:**
- `store_id` (Required): Unique identifier
- `name`: Store name
- `is_official`: Boolean flag
- `accepted`: Final acceptance status
- `call1/2/3_answered`: Call response tracking
- `call1/2/3_date`: Call dates
- `call1/2/3_observation`: Call notes
- `mail_sent`: Email communication flag
- `final_observation`: Acceptance notes

### Transient Models (Wizards)
- `crm.call.log.wizard`: One-off call logging
- `crm.send.mail.wizard`: Email sending interface
- `crm.bulk.import.wizard`: Bulk import interface

### Report Models
- `crm.store.report.acceptance`: Acceptance statistics
- `crm.store.report.calls`: Call response statistics

## Module Dependencies
- `base`: Core Odoo functionality
- `mail`: Email communication features

## Installation
1. Place module in your Odoo addons directory
2. Update module list
3. Install "CRM Store" module
4. System will automatically create all tables and views

## Testing

### Generate Sample Data
Navigate to Store form and use the action_generate_random method to create 20 sample stores for testing.

### CSV Sample
Use the provided sample data format to test bulk import functionality.

## Notes
- All dates default to today's date
- Call history is maintained separately for up to 3 calls
- Email addresses can be auto-populated from website field
- All operations are logged in Odoo's activity stream
