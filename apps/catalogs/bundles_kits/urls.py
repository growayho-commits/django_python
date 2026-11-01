from django.urls import path
from apps.catalogs.bundles_kits.views.bundles_kits_views import BundleKitAddAPIView

app_name = 'bundles_kits'
urlpatterns = [
    path('add/', BundleKitAddAPIView.as_view(), name='bundle-add'),
]
