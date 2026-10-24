from rest_framework import serializers
from apps.catalogs.reviews_ratings.models.reviews_ratings_profile import ReviewsRatingsProfile

class ReviewsRatingsProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewsRatingsProfile
        fields = '__all__'
