from django.db import models

class ReviewRatingProfile(models.Model):
    product_sku = models.CharField(max_length=100)
    reviewer_name = models.CharField(max_length=255)
    rating_score = models.PositiveIntegerField(default=5) # 1 to 5 stars
    comment = models.TextField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by {self.reviewer_name} - {self.rating_score} Stars"