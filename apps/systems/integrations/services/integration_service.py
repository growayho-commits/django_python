# apps/systems/integrations/services/integration_service.py

from ..models.integration_profile import IntegrationProfile

class IntegrationService:
    @staticmethod
    def get_integration_config(service_name):
        try:
            return IntegrationProfile.objects.get(service_name=service_name, is_active=True)
        except IntegrationProfile.DoesNotExist:
            raise ValueError(f"Active integration for {service_name} not found.")

    @staticmethod
    def update_or_create_integration(service_name, data):
        profile, created = IntegrationProfile.objects.update_or_create(
            service_name=service_name,
            defaults=data
        )
        return profile