from django.db import models
from django.conf import settings
from .business_profile import BusinessProfile

class UserRoleAssignment(models.Model):
    ROLE_CHOICES = [
        ('BUSINESS_STAFF', 'Business Staff (Member + Company Staff)'),
        ('EXECUTIVE', 'Platform Executive (Member + Superuser Staff)'),
        ('SELLER', 'Seller (Member + Seller Store)'),
        ('MERCHANT', 'Merchant (Member + B2B Merchant)'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='role_assignments')
    role_type = models.CharField(max_length=30, choices=ROLE_CHOICES)
    
    business = models.ForeignKey(
        BusinessProfile,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='staff_members'
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text="False என்றால் கூடுதல் பொறுப்பு துண்டிக்கப்பட்டு சாதாரண Member ஆக மாறுவார்"
    )
    
    assigned_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        status = "Active" if self.is_active else "Deactivated (Member Only)"
        return f"{self.user.email} -> {self.get_role_type_display()} [{status}]"