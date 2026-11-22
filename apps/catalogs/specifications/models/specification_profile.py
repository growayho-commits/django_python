from django.db import models

class SpecificationProfile(models.Model):
    title = models.CharField(max_length=255)
    value = models.TextField()
    unit = models.CharField(max_length=50, blank=True, null=True) # e.g., kg, cm, watts
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}: {self.value}"