from django.urls import path
from apps.catalogs.catalog_medias.views.catalog_media_views import CatalogMediaSaveAPIView

app_name = 'catalog_medias'
urlpatterns = [
    path('save/', CatalogMediaSaveAPIView.as_view(), name='media-save'),
]
