from django.db import models
from django.contrib.auth import get_user_model
from apps.professional_network.profiles.models.skill_profile import ProfessionalProfile
from apps.professional_network.enquiries.models.enquiry import SkillEnquiry

User = get_user_model()

class SkillRating(models.Model):
    enquiry = models.OneToOneField(SkillEnquiry, on_delete=models.CASCADE, related_name='rating')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_ratings')
    provider_profile = models.ForeignKey(ProfessionalProfile, on_delete=models.CASCADE, related_name='received_ratings')
    
    stars = models.PositiveIntegerField(choices=[(i, f"{i} Star") for i in range(1, 6)])
    feedback = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # ரேட்டிங் சேவ் ஆனவுடனே என்கொயரி ஆட்டோமேட்டிக்காக Completed (is_completed = True) ஆகிவிடும்
        super().save(*args, **kwargs)
        self.enquiry.is_completed = True
        self.enquiry.save()

    def __str__(self):
        return f"{self.stars} Stars - {self.provider_profile.skill_title}"