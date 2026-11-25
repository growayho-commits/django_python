from django.conf import settings
from django.db import models


class ReviewRatingProfile(models.Model):
    catalogue = models.ForeignKey(
        "core_catalogs.CoreCatalogProfile",
        on_delete=models.CASCADE,
        related_name="reviews",
        null=True,
        blank=True,
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="catalogue_reviews",
        null=True,
        blank=True,
    )
    product_sku = models.CharField(max_length=100, blank=True, default="")
    reviewer_name = models.CharField(max_length=255)
    rating_score = models.PositiveIntegerField(default=5)  # 1 to 5 stars
    comment = models.TextField(blank=True, null=True)
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by {self.reviewer_name} - {self.rating_score} Stars"