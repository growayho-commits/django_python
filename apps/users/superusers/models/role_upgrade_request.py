# E:\django_python\apps\users\superusers\models\role_upgrade_request.py

from django.db import models
from django.conf import settings


class RoleUpgradeRequest(models.Model):
    ROLE_CHOICES = (
        ('member', 'Member'),
        ('seller', 'Seller'),
        ('merchant', 'Merchant'),
        ('executive', 'Executive'),
    )
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('reconsidered', 'Reconsidered'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='role_upgrade_requests'
    )
    requested_role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    business_name = models.CharField(max_length=255, blank=True, null=True)
    gst_number = models.CharField(max_length=50, blank=True, null=True)
    admin_remarks = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} -> {self.requested_role} ({self.status})"