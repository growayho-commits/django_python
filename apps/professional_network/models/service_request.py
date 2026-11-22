from django.conf import settings
from django.db import models
from apps.professional_network.profiles.models.skill_profile import ProfessionalProfile

class ServiceRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='client_service_requests'
    )
    professional = models.ForeignKey(
        ProfessionalProfile, 
        on_delete=models.CASCADE, 
        related_name='received_service_requests'
    )
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        client_name = getattr(self.client, 'email', 'Client')
        prof_name = getattr(self.professional.user, 'email', 'Professional')
        return f"Request by {client_name} to {prof_name} [{self.status}]"