import requests
from django.conf import settings

class NotebookLMIntegrationService:
    def __init__(self):
        self.api_key = getattr(settings, 'NOTEBOOKLM_API_KEY', '')
        self.notebook_id = "notebooks/36d47b9a-9092-483b-8734-ed8ab14f2e14"
        self.endpoint = f"https://api.notebooklm.google.com/v1/{self.notebook_id}:query"

    def query_machine_manual(self, search_query):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "query": search_query
        }
        try:
            response = requests.post(self.endpoint, json=payload, headers=headers)
            if response.status_code == 200:
                return response.json().get('answer', 'தகவல் கிடைக்கவில்லை.')
            return "ஆவணத்தைத் தேடுவதில் பிழை ஏற்பட்டது."
        except Exception as e:
            return f"இணைப்புப் பிழை: {str(e)}"


# apps/systems/integrations/services/notebooklm_service.py
class NotebookLMIntegrationService:
    @staticmethod
    def query_enterprise_docs(query_text):
        response_data = {
            "query": query_text,
            "insights": "Industrial textile machinery documentation extracted successfully.",
            "status": "ACTIVE"
        }
        return response_data