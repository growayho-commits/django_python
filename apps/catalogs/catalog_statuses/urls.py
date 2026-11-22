from django.urls import path
from .views.catalog_status_views import CatalogStatusListCreateAPIView

app_name = 'catalog_statuses'

urlpatterns = [
    path('catalog-status-list-create-a-p-i/', CatalogStatusListCreateAPIView.as_view(), name='catalog_status_list_create_a_p_i'),
]
