from django.urls import path
from .views.rating_views import create_rating_view

app_name = 'ratings'

urlpatterns = [
    path('create-rating/', create_rating_view, name='create_rating'),
]
