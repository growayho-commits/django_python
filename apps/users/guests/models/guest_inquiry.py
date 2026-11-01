# apps/users/guests/models/guest_inquiry.py

from django.db import models
from django.utils.translation import gettext_lazy as _

class GuestInquiry(models.Model):
    """
    Guests அல்லது பார்வையாளர்கள் தளத்தின் மூலம் சமர்ப்பிக்கும் விசாரணைகள் (Inquiries).
    """
    full_name = models.CharField(max_length=150, verbose_name=_('Full Name'))
    email = models.EmailField(verbose_name=_('Email Address'))
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('Phone Number'))
    subject = models.CharField(max_length=255, verbose_name=_('Subject'))
    message = models.TextField(verbose_name=_('Message'))
    
    is_resolved = models.BooleanField(default=False, verbose_name=_('Is Resolved'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))

    class Meta:
        verbose_name = _('Guest Inquiry')
        verbose_name_plural = _('Guest Inquiries')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} - {self.subject}"