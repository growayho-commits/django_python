from django.db import models

class RoleRequirement(models.Model):
    ROLE_CHOICES = (
        ('merchant', 'Merchant'),
        ('seller', 'Seller'),
        ('executive', 'Executive'),
    )
    STATUS_CHOICES = (
        ('required', 'Required'),
        ('optional', 'Optional'),
        ('not_required', 'Not Required'),
    )
    
    role_name = models.CharField(max_length=50, choices=ROLE_CHOICES, unique=True)
    require_basic_profile = models.CharField(max_length=20, choices=STATUS_CHOICES, default='required')
    require_business_profile = models.CharField(max_length=20, choices=STATUS_CHOICES, default='optional')
    require_gst = models.CharField(max_length=20, choices=STATUS_CHOICES, default='optional')

    def __str__(self):
        return f"Role Config: {self.get_role_name_display()}"