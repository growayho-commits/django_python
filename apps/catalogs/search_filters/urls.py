from django.urls import path
from .views.search_filter_views import SearchFilterListCreateAPIView

app_name = 'search_filters'

urlpatterns = [
    path('search-filter-list-create-a-p-i/', SearchFilterListCreateAPIView.as_view(), name='search_filter_list_create_a_p_i'),
]
