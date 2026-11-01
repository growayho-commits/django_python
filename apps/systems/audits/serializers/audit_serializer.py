# apps/systems/audits/serializers/audit_serializer.py

from rest_framework import serializers
from ..models.audit_profile import AuditLogProfile

class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLogProfile
        fields = ['id', 'user', 'action', 'module_name', 'description', 'ip_address', 'created_at']
        read_only_fields = ['id', 'created_at']