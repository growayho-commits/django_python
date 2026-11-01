from django.urls import path, include

app_name = 'catalogs'

urlpatterns = [
    path('core/', include('apps.catalogs.core_catalogs.urls', namespace='core_catalogs')),
    path('pricing/', include('apps.catalogs.pricing_tiers.urls', namespace='pricing_tiers')),
    path('inventory/', include('apps.catalogs.inventories.urls', namespace='inventories')),
    path('categories/', include('apps.catalogs.categories.urls', namespace='categories')),
    path('attributes/', include('apps.catalogs.attributes.urls', namespace='attributes')),
    path('variants/', include('apps.catalogs.variants.urls', namespace='variants')),
    path('media/', include('apps.catalogs.catalog_medias.urls', namespace='catalog_medias')),
    path('status/', include('apps.catalogs.catalog_statuses.urls', namespace='catalog_statuses')),
    path('specifications/', include('apps.catalogs.specifications.urls', namespace='specifications')),
    path('bundles/', include('apps.catalogs.bundles_kits.urls', namespace='bundles_kits')),
    path('search-filters/', include('apps.catalogs.search_filters.urls', namespace='search_filters')),
    #path('wishlist/', include('apps.catalogs.wishlists.urls', namespace='wishlists')),
    path('reviews/', include('apps.catalogs.reviews_ratings.urls', namespace='reviews_ratings')),
]


# apps/catalogs/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# சப்-ஆப் வியூசெட்களை இங்கு இம்போர்ட் செய்ய வேண்டும்
# எ.கா: from apps.catalogs.core_catalogs.views import CoreCatalogViewSet
# from apps.catalogs.variants.views import CatalogVariantViewSet

router = DefaultRouter()
# router.register(r'core-catalogs', CoreCatalogViewSet, basename='core-catalog')
# router.register(r'variants', CatalogVariantViewSet, basename='catalog-variant')

urlpatterns = [
    path('', include(router.urls)),
]