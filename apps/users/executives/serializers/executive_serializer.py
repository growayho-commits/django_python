from rest_framework import serializers
from apps.users.executives.models import ExecutiveProfile

class ExecutiveProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExecutiveProfile
        fields = ['id', 'user', 'employee_id', 'executive_type', 'assigned_region', 'is_active_agent', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']