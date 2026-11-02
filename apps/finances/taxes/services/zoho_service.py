import requests
from django.conf import settings
from apps.finances.taxes.models import TaxProfile[cite: 1]
from apps.marketing_leads.orders.models import OrderProfile[cite: 1]

class ZohoBooksService:
    def __init__(self):
        self.auth_token = getattr(settings, 'ZOHO_BOOKS_AUTH_TOKEN', '')
        self.organization_id = getattr(settings, 'ZOHO_ORGANIZATION_ID', '')
        self.base_url = "https://www.zohoapis.com/books/v3"
        self.headers = {
            "Authorization": f"Zoho-oauthtoken {self.auth_token}",
            "Content-Type": "application/json"
        }

    def sync_gst_invoice(self, order_id):
        try:
            order = OrderProfile.objects.get(id=order_id)
            payload = {
                "customer_name": order.user.get_full_name() or order.user.username,
                "date": order.created_at.strftime('%Y-%m-%d'),
                "gst_treatment": "business_gst",
                "line_items": [
                    {
                        "name": item.catalog.name,
                        "rate": float(item.price),
                        "quantity": item.quantity,
                        "tax_id": getattr(settings, 'ZOHO_GST_TAX_ID', '')
                    } for item in order.items.all()
                ]
            }
            url = f"{self.base_url}/invoices?organization_id={self.organization_id}"
            response = requests.post(url, json=payload, headers=self.headers)
            response_data = response.json()
            
            if response.status_code == 201 and response_data.get('code') == 0:
                return {"status": "SUCCESS", "invoice_id": response_data['invoice']['invoice_id']}
            return {"status": "FAILED", "error": response_data.get('message')}
        except OrderProfile.DoesNotExist:
            return {"status": "FAILED", "error": "Order not found"}
        except Exception as e:
            return {"status": "ERROR", "error": str(e)}