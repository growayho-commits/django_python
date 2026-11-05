from django.urls import path
from apps.catalogs.core_catalogs.views import core_catalog_views

app_name = 'core_catalogs'

urlpatterns = [
    path('products/', core_catalog_views.CoreCatalogCreateListView.as_view(), name='product-list-create'),
]