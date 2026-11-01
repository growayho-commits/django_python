# apps/catalogs/reviews_ratings/serializers/review_serializer.py

from rest_framework import serializers
from apps.catalogs.reviews_ratings.models.review_profile import CatalogReviewProfile

class CatalogReviewProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogReviewProfile
        fields = ['id', 'catalog', 'user_identifier', 'rating', 'comment', 'is_approved', 'created_at']
        read_only_fields = ['id', 'created_at']