from django.db import models

class ProfessionalProfile(models.Model):
    # உங்களது புராஜெக்ட்க்குத் தேவையான ஃபீல்டுகள்
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title