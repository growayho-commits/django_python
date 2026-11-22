from apps.catalogs.reviews_ratings.models.review_rating_profile import ReviewRatingProfile

class ReviewRatingApplicationService:
    @staticmethod
    def get_all_reviews():
        return ReviewRatingProfile.objects.all()

    @staticmethod
    def create_review(validated_data):
        return ReviewRatingProfile.objects.create(**validated_data)