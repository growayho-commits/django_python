from django.db import models
from django.contrib.auth import get_user_model
from apps.professional_network.profiles.models.skill_profile import ProfessionalProfile

User = get_user_model()

class SkillEnquiry(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_enquiries')
    provider_profile = models.ForeignKey(ProfessionalProfile, on_delete=models.CASCADE, related_name='received_enquiries')
    message = models.TextField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Enquiry by {self.sender.username} to {self.provider_profile.skill_title}"