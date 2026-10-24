from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from .professional_profile import UserProfessionalProfile


class UserReview(models.Model):
    """
    தொழில் வல்லுநர்களுக்கு (Professionals) வழங்கப்படும் ஸ்டார் ரேட்டிங் மற்றும் விமர்சனங்கள்.
    """
    professional = models.ForeignKey(
        UserProfessionalProfile,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="given_reviews"
    )
    rating = models.PositiveIntegerField(
        _("Star Rating"),
        default=5,
        help_text=_("1 முதல் 5 வரையிலான ஸ்டார் ரேட்டிங்")
    )
    comment = models.TextField(_("Review Comment"), blank=True)
    is_completed = models.BooleanField(_("Service Completed"), default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("User Review")
        verbose_name_plural = _("User Reviews")
        db_table = "users_review"

    def __str__(self):
        return f"{self.rating} Stars for {self.professional.user.email} by {self.reviewer.email}"