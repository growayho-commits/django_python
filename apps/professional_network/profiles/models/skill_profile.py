from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

SERVICE_SCOPE_CHOICES = [
    ('online', 'Online / Remote Service'),
    ('pincode', 'Specific Pincode(s)'),
    ('taluk', 'Specific Taluk(s)'),
    ('district', 'Specific District(s)'),
    ('state', 'Specific State(s)'),
    ('all_india', 'All India'),
    ('worldwide', 'Worldwide'),
]


class ProfessionalProfile(models.Model):
    APPROVAL_STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='professional_skills')
    service_category = models.ForeignKey(
        'service_categries.ServiceCategory',
        on_delete=models.SET_NULL,
        related_name='provider_profiles',
        null=True,
        blank=True,
    )
    skill_title = models.CharField(max_length=150)
    hsn_service_code = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField()
    experience_years = models.PositiveIntegerField(default=0)
    starting_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    city = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    delivery_scope = models.CharField(
        max_length=30,
        choices=SERVICE_SCOPE_CHOICES,
        default='district',
    )
    delivery_locations = models.JSONField(default=list, blank=True)
    approval_status = models.CharField(
        max_length=20,
        choices=APPROVAL_STATUS_CHOICES,
        default='pending',
    )
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.skill_title} ({self.approval_status})"


class ProfessionalMedia(models.Model):
    MEDIA_TYPES = (
        ('image', 'Photo'),
        ('video', '1-Min Video/Reel'),
    )
    profile = models.ForeignKey(ProfessionalProfile, on_delete=models.CASCADE, related_name='galleries')
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES)
    file = models.FileField(upload_to='professionals/media/')
    caption = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class ProfessionalStory(models.Model):
    profile = models.ForeignKey(ProfessionalProfile, on_delete=models.CASCADE, related_name='stories')
    title = models.CharField(max_length=200)
    content = models.TextField()
    cover_image = models.ImageField(upload_to='professionals/stories/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk and self.profile.stories.count() >= 10:
            raise ValueError("Story limit reached! Maximum 10 stories allowed.")
        super().save(*args, **kwargs)


class ProfessionalEvent(models.Model):
    profile = models.ForeignKey(ProfessionalProfile, on_delete=models.CASCADE, related_name='events')
    event_name = models.CharField(max_length=200)
    description = models.TextField()
    event_date = models.DateTimeField()
    location = models.CharField(max_length=255)
    banner = models.ImageField(upload_to='professionals/events/', null=True, blank=True)
    is_active = models.BooleanField(default=True)