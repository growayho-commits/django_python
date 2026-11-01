from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ProfessionalProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='professional_skills')
    skill_title = models.CharField(max_length=150) # எ.கா: Industrial Electrician / Tuition Master
    hsn_service_code = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField()
    experience_years = models.PositiveIntegerField(default=0)
    city = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.skill_title}"

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