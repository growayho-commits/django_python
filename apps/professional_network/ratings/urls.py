from django.urls import path
from apps.professional_network.ratings.views import create_rating_view

app_name = 'ratings'

urlpatterns = [
    path('add/<int:enquiry_id>/', create_rating_view, name='add_rating'),
]