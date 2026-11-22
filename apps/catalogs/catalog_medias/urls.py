from django.urls import path
from .views.catalog_media_views import CatalogMediaListCreateAPIView

app_name = 'catalog_medias'

urlpatterns = [
    path('catalog-media-list-create-a-p-i/', CatalogMediaListCreateAPIView.as_view(), name='catalog_media_list_create_a_p_i'),
]
