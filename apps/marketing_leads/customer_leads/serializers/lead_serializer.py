# apps/marketing_leads/customer_leads/serializers/lead_serializer.py

from rest_framework import serializers
from ..models.lead_profile import CustomerLeadProfile

class CustomerLeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerLeadProfile
        fields = ['id', 'full_name', 'email', 'phone_number', 'status', 'source', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']