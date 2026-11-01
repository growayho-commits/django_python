# apps/catalogs/reviews_ratings/models/review_profile.py

from django.db import models
from apps.catalogs.core_catalogs.models.core_catalog_profile import CoreCatalog

class CatalogReviewProfile(models.Model):
    catalog = models.ForeignKey(CoreCatalog, on_delete=models.CASCADE, related_name='reviews')
    user_identifier = models.CharField(max_length=150) # வாடிக்கையாளரின் ஐடி அல்லது பெயர்
    rating = models.PositiveSmallIntegerField(default=5) # 1 முதல் 5 வரை ரேட்டிங்
    comment = models.TextField(blank=True, null=True)
    is_approved = models.BooleanField(default=True) # நிர்வாகி ஒப்புதல் அளித்ததுதானா என்பதைச் சரிபார்க்க
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.catalog.name} - Rating: {self.rating}/5"