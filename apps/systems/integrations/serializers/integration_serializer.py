# apps/systems/integrations/serializers/integration_serializer.py

from rest_framework import serializers
from ..models.integration_profile import IntegrationProfile

class IntegrationProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntegrationProfile
        fields = ['id', 'service_name', 'api_key', 'api_secret', 'webhook_url', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'api_secret': {'write_only': True}  # Security: hide secret on read
        }