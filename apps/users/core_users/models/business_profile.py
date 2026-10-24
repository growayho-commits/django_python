from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class BusinessEnterpriseProfile(models.Model):
    """
    4. பிசினஸ் ப்ரொஃபைல் (Business & Enterprise Profile)
    நிறுவனத்தின் பெயர், ஜிஎஸ்டி மற்றும் வணிகத் தரவுகள்.
    """
    BUSINESS_TYPE_CHOICES = (
        ("PROPRIETORSHIP", _("Sole Proprietorship")),
        ("PARTNERSHIP", _("Partnership Firm")),
        ("PVT_LTD", _("Private Limited")),
        ("MERCHANT", _("Merchant / Trader")),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="business_profile"
    )
    company_name = models.CharField(_("Business / Company Legal Name"), max_length=200)
    gst_number = models.CharField(_("Tax / GST / VAT Identification Numbers"), max_length=50, blank=True, db_index=True)
    business_type = models.CharField(_("Business Type"), max_length=30, choices=BUSINESS_TYPE_CHOICES, default="PROPRIETORSHIP")
    billing_currency = models.CharField(_("Billing Currency"), max_length=10, default="INR")
    registered_office_address = models.TextField(_("Branch / Warehouse Locations & Address"), blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Business Enterprise Profile")
        verbose_name_plural = _("Business Enterprise Profiles")
        db_table = "users_business_profile"

    def __str__(self):
        identifier = getattr(self.user, 'email', getattr(self.user, 'username', str(self.user.pk)))
        c_name = self.company_name or "Unnamed Company"
        return f"{c_name} ({identifier})"