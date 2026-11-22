from rest_framework import serializers
from apps.catalogs.reviews_ratings.models.review_rating_profile import ReviewRatingProfile

class ReviewRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewRatingProfile
        fields = ['id', 'product_sku', 'reviewer_name', 'rating_score', 'comment', 'is_approved', 'created_at', 'updated_at']