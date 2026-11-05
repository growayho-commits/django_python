from django.db import models
from django.contrib.auth import get_user_model
from apps.professional_network.models.professional_profile import ProfessionalProfile

User = get_user_model()

class ServiceRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_service_requests')
    professional = models.ForeignKey(ProfessionalProfile, on_delete=models.CASCADE, related_name='received_service_requests')
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Request by {self.client.username} to {self.professional.user.username} [{self.status}]"