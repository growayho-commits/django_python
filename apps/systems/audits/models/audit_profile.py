# apps/systems/audits/models/audit_profile.py

from django.conf import settings
from django.db import models

class AuditLogProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_logs')
    action = models.CharField(max_length=255)  # e.g., 'CREATE', 'UPDATE', 'DELETE'
    module_name = models.CharField(max_length=100)  # e.g., 'Orders', 'Carts', 'Users'
    description = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        user_str = self.user.email if self.user else "System / Anonymous"
        return f"[{self.created_at}] {user_str} - {self.action} on {self.module_name}"