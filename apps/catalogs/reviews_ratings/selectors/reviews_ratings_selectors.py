from apps.catalogs.reviews_ratings.models.reviews_ratings_profile import ReviewsRatingsProfile

class ReviewsRatingsSelector:
    @staticmethod
    def get_reviews_by_catalog(catalog_id: str):
        return ReviewsRatingsProfile.objects.filter(catalog_id=catalog_id)
