# Store CRM

A simple CRM module for managing store contacts and follow-ups in Odoo 19.

## Features

- Store contact management
- Call logging (up to 3 calls per store)
- Email communication tracking
- Acceptance status tracking
- Communication channel preferences (WhatsApp, Viber, Telegram)

## Installation

1. Place the `addon_crm` folder in your Odoo addons directory
2. Update your Odoo configuration to include the addons path
3. Install the module from the Odoo Apps menu

## Usage

1. Navigate to Store CRM in the main menu
2. Create new store records
3. Use the "Log Call" button to record call attempts
4. Use the "Send Mail" button to send emails
5. Track acceptance status and communication history

## Views

- **List View**: Overview of all stores
- **Form View**: Detailed store information with call history
- **Kanban View**: Visual status overview
- **Search**: Filter by status, official status, etc.

---

### Create Records

* Click **Create**
* Fill store details
* Track calls and final decision

---

### Generate Demo Data

Click the button:

```
Generate Random
```

This will automatically create multiple fake CRM records for testing.

---

## 🗂️ Data Structure

### 🟦 Main Info

* Store ID
* Slug
* Name
* Official flag
* Announcement ID
* Website / Phone / Logo

### 💬 Messaging

* WhatsApp
* Viber
* Telegram

### ☎️ Calls Tracking

Each call includes:

* Answered (boolean)
* Date
* Observation

(Call 1, Call 2, Call 3)

### 🏁 Final

* Accepted
* Mail Sent
* Final Observation

---

## 🏗️ Technical Details

* Model: `crm.store`
* Views:

  * list (list)
  * Form (notebook with sections)
* Server Method:

  * `action_generate_random()`

---

## 🔐 Access Control

| Role | Permissions |
| ---- | ----------- |
| User | Full CRUD   |

---

## ⚡ Development Notes

* Built for **Odoo 19**
* Simple architecture (no external dependencies)
* Easily extendable

---

## 🧩 Possible Improvements

* Kanban pipeline view
* Assign salespeople
* Automated call reminders
* Email integration
* API sync with external marketplaces
* Dashboard & reporting

---

## 👨‍💻 Author

Your Name

---

## 📄 License

MIT License (or your preferred license)

