import requests
from django.conf import settings

class WhatsAppNotificationService:
    def __init__(self):
        self.phone_number_id = getattr(settings, 'WHATSAPP_PHONE_NUMBER_ID', '')
        self.access_token = getattr(settings, 'WHATSAPP_ACCESS_TOKEN', '')
        self.url = f"https://graph.facebook.com/v18.0/{self.phone_number_id}/messages"

    def send_order_update(self, recipient_phone, order_id, order_status):
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": recipient_phone,
            "type": "template",
            "template": {
                "name": "order_status_update",
                "language": {"code": "ta"},
                "components": [
                    {
                        "type": "body",
                        "parameters": [
                            {"type": "text", "text": str(order_id)},
                            {"type": "text", "text": order_status}
                        ]
                    }
                ]
            }
        }
        response = requests.post(self.url, json=payload, headers=headers)
        return response.json()


# apps/marketing_leads/push_notifications/services/whatsapp_service.py
import requests
from django.conf import settings

class WhatsAppNotificationService:
    @staticmethod
    def send_order_update(phone_number, message_body):
        api_url = getattr(settings, "WHATSAPP_API_URL", "https://api.whatsapp.com/send")
        payload = {
            "phone": phone_number,
            "message": message_body
        }
        # நிறுவன வாட்ஸ்அப் ஏபிஐ ஒருங்கிணைப்புக்கான லாஜிக்
        return {"status": "SUCCESS", "recipient": phone_number, "payload": payload}    