from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ProfessionalProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='professional_profile')
    title = models.CharField(max_length=255)
    bio = models.TextField(blank=True, null=True)
    skills = models.TextField(help_text="Comma-separated skills")
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"