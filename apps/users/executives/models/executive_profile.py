from django.conf import settings
from django.db import models


class ExecutiveProfile(models.Model):
    EXECUTIVE_TYPES = (
        ('field_officer', 'Field Officer'),
        ('marketing_promoter', 'Marketing Promoter'),
        ('support_lead', 'Support Lead'),
    )

    ACTIVITY_CHOICES = (
        ('marketing', 'Marketing Activities'),
        ('logistics', 'Logistics Activities'),
        ('accounts', 'Accounts & Finance Activities'),
        ('onboarding', 'Vendor Onboarding'),
        ('inspections', 'Field Inspections'),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='executive_profile',
    )
    employee_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    executive_type = models.CharField(max_length=50, choices=EXECUTIVE_TYPES, default='field_officer')
    assigned_region = models.CharField(max_length=100, blank=True, null=True)
    assigned_activities = models.JSONField(default=list, blank=True)
    is_active_agent = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.employee_id:
            self.employee_id = f"EXE-{self.user_id}"
        super().save(*args, **kwargs)

    def has_activity(self, activity_code):
        return activity_code in (self.assigned_activities or [])

    def __str__(self):
        return f"{self.user.email} ({self.get_executive_type_display()})"