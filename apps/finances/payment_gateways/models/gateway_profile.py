from django.db import models

class PaymentGatewayConfig(models.Model):
    gateway_name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=False)
    api_key = models.CharField(max_length=255)
    api_secret = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.gateway_name