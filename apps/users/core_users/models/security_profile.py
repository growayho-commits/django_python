from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserSecurityProfile(models.Model):
    """
    5. செக்யூரிட்டி & கம்பையன்ஸ் ப்ரொஃபைல் (Security & Compliance Profile)
    2FA, கணக்கு நிலை, லாகின் ஐபி மற்றும் தணிக்கைப் பதிவுகள் (Audit Logs).
    """
    ACCOUNT_STATUS_CHOICES = (
        ("ACTIVE", _("Active")),
        ("SUSPENDED", _("Suspended")),
        ("BLOCKED", _("Blocked")),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="security_profile"
    )
    is_2fa_enabled = models.BooleanField(_("Two-Factor Authentication (2FA) Status"), default=False)
    last_login_ip = models.GenericIPAddressField(_("Last Login IP / Active Sessions"), blank=True, null=True)
    failed_login_attempts = models.PositiveIntegerField(_("Failed Login Attempts"), default=0)
    account_status = models.CharField(_("Account Status & Audit Logs"), max_length=20, choices=ACCOUNT_STATUS_CHOICES, default="ACTIVE")
    data_privacy_consent = models.BooleanField(_("Data Privacy Consent (GDPR/CCPA)"), default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("User Security Profile")
        verbose_name_plural = _("User Security Profiles")
        db_table = "users_security_profile"

    def __str__(self):
        return f"Security Profile for {self.user.email}"