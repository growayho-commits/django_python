from django.conf import settings
from django.db import models

class ExecutiveProfile(models.Model):
    EXECUTIVE_TYPES = (
        ('field_officer', 'Field Officer'),
        ('marketing_promoter', 'Marketing Promoter'),
        ('support_lead', 'Support Lead'),
    )
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='executive_profile')
    employee_id = models.CharField(max_length=50, unique=True)
    executive_type = models.CharField(max_length=50, choices=EXECUTIVE_TYPES, default='field_officer')
    assigned_region = models.CharField(max_length=100, blank=True, null=True)
    is_active_agent = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.get_executive_type_display()})"