from django.urls import path
from .views.core_catalog_views import CoreCatalogListCreateAPIView

app_name = 'core_catalogs'

urlpatterns = [
    path('core-catalog-list-create-a-p-i/', CoreCatalogListCreateAPIView.as_view(), name='core_catalog_list_create_a_p_i'),
]
