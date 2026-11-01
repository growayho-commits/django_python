from django.urls import path
from apps.professional_network.search_engine.views import directory_home_view, professional_search_view

app_name = 'search_engine'

urlpatterns = [
    path('', directory_home_view, name='directory_home'),
    path('results/', professional_search_view, name='search_results'),
]