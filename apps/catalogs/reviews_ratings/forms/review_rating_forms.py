from django import forms
from apps.catalogs.reviews_ratings.models.review_rating_profile import ReviewRatingProfile

class ReviewRatingAdminForm(forms.ModelForm):
    class Meta:
        model = ReviewRatingProfile
        fields = ['product_sku', 'reviewer_name', 'rating_score', 'comment', 'is_approved']