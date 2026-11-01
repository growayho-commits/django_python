# apps/catalogs/reviews_ratings/services/review_service.py

from apps.catalogs.reviews_ratings.models.review_profile import CatalogReviewProfile

class CatalogReviewService:
    @staticmethod
    def create_review(validated_data):
        """புதிய வாடிக்கையாளர் மதிப்புரையைச் சேர்க்க (Add Review)"""
        return CatalogReviewProfile.objects.create(**validated_data)

    @staticmethod
    def update_review(review_id, validated_data):
        """மதிப்புரையின் விவரங்களைப் புதுப்பிக்க (Edit / Update)"""
        try:
            review = CatalogReviewProfile.objects.get(id=review_id)
            for key, value in validated_data.items():
                setattr(review, key, value)
            review.save()
            return review
        except CatalogReviewProfile.DoesNotExist:
            raise ValueError("Review profile does not exist.")