import random
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class OTPVerification(models.Model):
    class ChannelChoices(models.TextChoices):
        EMAIL = 'EMAIL', _('மின்னஞ்சல் (Email)')
        SMS = 'SMS', _('குறுஞ்செய்தி (SMS)')
        WHATSAPP = 'WHATSAPP', _('வாட்ஸ்அப் (WhatsApp)')

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='otps',
        null=True, blank=True
    )
    channel = models.CharField(max_length=10, choices=ChannelChoices.choices)
    recipient = models.CharField(max_length=255, db_index=True)  # Email அல்லது Phone number
    otp_code = models.CharField(max_length=6)
    
    is_verified = models.BooleanField(default=False)
    attempts = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        verbose_name = _('OTP சரிபார்ப்பு')
        verbose_name_plural = _('OTP சரிபார்ப்புகள் (OTP Verifications)')
        indexes = [
            models.Index(fields=['recipient', 'channel', 'is_verified']),
        ]

    def save(self, *args, **kwargs):
        if not self.otp_code:
            self.otp_code = f"{random.randint(100000, 999999)}"
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(minutes=10)
        super().save(*args, **kwargs)

    def is_valid(self):
        return not self.is_verified and timezone.now() <= self.expires_at

    def __str__(self):
        return f"{self.channel} - {self.recipient} [{self.otp_code}]"