from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class AdditionalProfile(models.Model):
    """
    பயனருக்கான கூடுதல் விவரங்கள் அல்லது ப்ரொஃபைல் தகவல்
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="additional_profile"
    )
    bio = models.TextField(_("Bio / Description"), blank=True, null=True)
    website = models.URLField(_("Website"), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Additional Profile")
        verbose_name_plural = _("Additional Profiles")
        db_table = "users_additional_profile"

    def __str__(self):
        identifier = getattr(self.user, 'email', getattr(self.user, 'username', str(self.user.pk)))
        return f"Additional Profile for {identifier}"