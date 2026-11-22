from apps.catalogs.reviews_ratings.models.review_rating_profile import ReviewRatingProfile

def get_approved_reviews():
    return ReviewRatingProfile.objects.filter(is_approved=True)