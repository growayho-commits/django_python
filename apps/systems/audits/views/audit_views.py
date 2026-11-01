# apps/systems/audits/views/audit_views.py

from rest_framework import viewsets, permissions
from ..models.audit_profile import AuditLogProfile
from ..serializers.audit_serializer import AuditLogSerializer

class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLogProfile.objects.all().order_by('-created_at')
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAdminUser]