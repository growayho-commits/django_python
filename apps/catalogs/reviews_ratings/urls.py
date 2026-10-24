from django.urls import path
from apps.catalogs.reviews_ratings.views.reviews_ratings_views import ReviewCreateAPIView

app_name = 'reviews_ratings'
urlpatterns = [
    path('post/', ReviewCreateAPIView.as_view(), name='review-post'),
]
