# apps/marketing_leads/customer_leads/services/lead_service.py

from ..models.lead_profile import CustomerLeadProfile

class CustomerLeadService:
    @staticmethod
    def create_lead(data):
        lead = CustomerLeadProfile.objects.create(**data)
        return lead

    @staticmethod
    def update_lead_status(lead_id, status):
        try:
            lead = CustomerLeadProfile.objects.get(id=lead_id)
            lead.status = status
            lead.save()
            return lead
        except CustomerLeadProfile.DoesNotExist:
            raise ValueError("Customer lead profile not found.")