# apps/systems/audits/services/audit_service.py

from ..models.audit_profile import AuditLogProfile

class AuditService:
    @staticmethod
    def log_action(action, module_name, user=None, description=None, ip_address=None):
        audit_log = AuditLogProfile.objects.create(
            user=user if user and user.is_authenticated else None,
            action=action,
            module_name=module_name,
            description=description,
            ip_address=ip_address
        )
        return audit_log