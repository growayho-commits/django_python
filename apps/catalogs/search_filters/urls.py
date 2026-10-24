from django.urls import path
from apps.catalogs.search_filters.views.search_filters_views import SearchFiltersSaveAPIView

app_name = 'search_filters'
urlpatterns = [
    path('save/', SearchFiltersSaveAPIView.as_view(), name='search-filters-save'),
]
