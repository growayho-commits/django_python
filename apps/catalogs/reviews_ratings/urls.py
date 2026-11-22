from django.urls import path
from .views.review_rating_views import ReviewRatingListCreateAPIView

app_name = 'reviews_ratings'

urlpatterns = [
    path('review-rating-list-create-a-p-i/', ReviewRatingListCreateAPIView.as_view(), name='review_rating_list_create_a_p_i'),
]
