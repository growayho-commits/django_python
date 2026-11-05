from django.db import models
from django.conf import settings

class SuperuserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='superuser_profile')
    security_level = models.CharField(max_length=50, default='Administrator')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Superuser Profile: {self.user.email}"