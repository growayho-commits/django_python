from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class SearchLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    query_text = models.CharField(max_length=255)
    location_text = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)