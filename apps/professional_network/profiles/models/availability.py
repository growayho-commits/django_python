from django.db import models
from .skill_profile import ProfessionalProfile

class ProviderAvailability(models.Model):
    profile = models.OneToOneField(ProfessionalProfile, on_delete=models.CASCADE, related_name='availability')
    is_available = models.BooleanField(default=True)
    is_on_leave = models.BooleanField(default=False)
    working_hours = models.CharField(max_length=100, default="9:00 AM - 6:00 PM")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        status = "On Leave" if self.is_on_leave else ("Available" if self.is_available else "Busy")
        return f"{self.profile.skill_title} - {status}"