from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserCredentialProfile(models.Model):
    """
    1. பேசிக் ப்ரொஃபைல் (Basic Profile - Signup & Assignment)
    மின்னஞ்சல், பாஸ்வேர்ட், அசைன் செய்யப்பட்ட மெர்ச்சன்ட் மற்றும் OTP சரிபார்ப்பு.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="credential_profile"
    )
    assigned_merchant_email = models.EmailField(
        _("Assigned Merchant / Supervisor Email"),
        blank=True,
        null=True,
        db_index=True,
        help_text=_("பதிவு செய்யும் போதே இணையும் மெர்ச்சன்ட் அல்லது சூப்பர்வைசர் மின்னஞ்சல்")
    )
    is_email_verified = models.BooleanField(
        _("OTP Verification Status"),
        default=False,
        help_text=_("ஈமெயில் அல்லது மொபைல் OTP மூலம் உறுதிப்படுத்தப்பட்டதா")
    )
    otp_code = models.CharField(
        _("OTP Code"),
        max_length=6,
        blank=True,
        null=True
    )
    otp_created_at = models.DateTimeField(
        _("OTP Created At"),
        blank=True,
        null=True
    )
    terms_accepted = models.BooleanField(
        _("Terms & Conditions Acceptance"),
        default=False,
        help_text=_("விதிமுறைகள் மற்றும் நிபந்தனைகளுக்கு ஒப்புதல் அளிக்கப்பட்டதா")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("User Credential Profile")
        verbose_name_plural = _("User Credential Profiles")
        db_table = "users_credential_profile"

    def __str__(self):
        return f"Credential Profile for {self.user.email}"