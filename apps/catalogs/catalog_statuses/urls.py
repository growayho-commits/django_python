from django.urls import path
from apps.catalogs.catalog_statuses.views.catalog_status_views import CatalogStatusUpdateAPIView

app_name = 'catalog_statuses'
urlpatterns = [
    path('update/', CatalogStatusUpdateAPIView.as_view(), name='status-update'),
]
