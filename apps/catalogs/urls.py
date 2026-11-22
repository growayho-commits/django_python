from django.urls import path, include

app_name = 'catalogs'

urlpatterns = [
    path('attributes/', include('apps.catalogs.attributes.urls')),
    path('bundles_kits/', include('apps.catalogs.bundles_kits.urls')),
    path('catalog_medias/', include('apps.catalogs.catalog_medias.urls')),
    path('catalog_statuses/', include('apps.catalogs.catalog_statuses.urls')),
    path('catalog_wishlist/', include('apps.catalogs.catalog_wishlist.urls')),
    path('categories/', include('apps.catalogs.categories.urls')),
    path('core_catalogs/', include('apps.catalogs.core_catalogs.urls')),
    path('inventories/', include('apps.catalogs.inventories.urls')),
    path('pricing_extras/', include('apps.catalogs.pricing_extras.urls')),
    path('pricing_tiers/', include('apps.catalogs.pricing_tiers.urls')),
    path('reviews_ratings/', include('apps.catalogs.reviews_ratings.urls')),
    path('search_filters/', include('apps.catalogs.search_filters.urls')),
    path('specifications/', include('apps.catalogs.specifications.urls')),
    path('variants/', include('apps.catalogs.variants.urls')),
]
