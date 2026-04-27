import requests
from odoo import fields, models
from odoo.exceptions import UserError

GRAPHQL_URL = "https://api.ouedkniss.com/graphql"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}


class MyLeadBulkWizard(models.TransientModel):
    _name = "my.lead.bulk.wizard"
    _description = "Import from Ouedkniss"

    category_slug = fields.Char(
        string="Category",
        required=True,
        default="immobilier",
        help="e.g. immobilier, informatique, vehicules",
    )
    page = fields.Integer(string="Page", default=1)
    count = fields.Integer(string="Count", default=20)

    def _fetch_stores(self):
        payload = {
            "query": """
                query SearchQuery($filter: SearchFilterInput) {
                    search(filter: $filter) {
                        announcements {
                            data {
                                id
                                store {
                                    id
                                    name
                                    slug
                                    imageUrl
                                    isOfficial
                                }
                            }
                        }
                    }
                }
            """,
            "variables": {
                "filter": {
                    "categorySlug": self.category_slug,
                    "origin": "STORE",
                    "connected": False,
                    "page": self.page,
                    "count": self.count,
                },
            },
        }
        resp = requests.post(GRAPHQL_URL, json=payload, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        announcements = (
            resp.json()
            .get("data", {})
            .get("search", {})
            .get("announcements", {})
            .get("data", [])
        )
        # one announcement per store — keep first occurrence
        store_map = {}
        for ann in announcements:
            store = ann.get("store")
            if not store:
                continue
            sid = store["id"]
            if sid not in store_map:
                store_map[sid] = {
                    "store_id": str(sid),
                    "name": store.get("name"),
                    "slug": store.get("slug"),
                    "image_url": store.get("imageUrl"),
                    "is_official": store.get("isOfficial", False),
                    "announcement_id": str(ann["id"]),
                }
        return store_map

    def _fetch_phone(self, announcement_id):
        payload = {
            "query": """
                query UnhidePhone($id: ID!) {
                    phones: announcementPhoneGet(id: $id) {
                        phone
                        hasWhatsapp
                        hasTelegram
                        hasViber
                    }
                }
            """,
            "variables": {"id": announcement_id},
        }
        try:
            resp = requests.post(GRAPHQL_URL, json=payload, headers=HEADERS, timeout=10)
            resp.raise_for_status()
            phones = resp.json().get("data", {}).get("phones", [])
            if phones:
                return phones[0]
        except Exception:
            pass
        return {}

    def action_import(self):
        store_map = self._fetch_stores()
        if not store_map:
            raise UserError(
                f'No stores found for "{self.category_slug}" page {self.page}.'
            )

        vals_list = []
        for store in store_map.values():
            phone_data = self._fetch_phone(store["announcement_id"])
            vals_list.append(
                {
                    **store,
                    "phone": phone_data.get("phone"),
                    "has_whatsapp": phone_data.get("hasWhatsapp", False),
                    "has_telegram": phone_data.get("hasTelegram", False),
                    "has_viber": phone_data.get("hasViber", False),
                }
            )

        created = self.env["my.lead"].create(vals_list)
        return {
            "type": "ir.actions.act_window",
            "name": f"Imported {len(created)} stores",
            "res_model": "my.lead",
            "view_mode": "list,form",
            "domain": [("id", "in", created.ids)],
            "target": "current",
        }
