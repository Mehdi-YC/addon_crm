# 📞 CRM Store (Odoo 19 Module)

A custom CRM module for managing store leads, tracking call attempts, and handling final conversion status.

---

## 🚀 Features

* 🏪 Store management (ID, name, slug, website, phone)
* 📢 Announcement tracking
* 💬 Messaging availability (WhatsApp, Viber, Telegram)
* ☎️ Multi-step call tracking (3 call attempts)
* 📝 Observations per call
* 🏁 Final decision tracking (Accepted / Mail Sent)
* ⚡ One-click **random data generator**
* 📋 List view + detailed form view

---

## 📦 Installation

1. Copy the module into your Odoo addons directory:

```bash
addons/crm_store
```

2. Restart Odoo:

```bash
./odoo-bin -u crm_store
```

3. Activate developer mode (optional but recommended)

4. Go to:

```
Apps → Search "CRM Store" → Install
```

---

## 🧭 Usage

### Access Module

```
Store CRM → Stores
```

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

