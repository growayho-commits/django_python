from django.urls import path
from apps.catalogs.bundles_kits.views.bundle_kit_views import BundleKitListCreateAPIView

urlpatterns = [
    path('', BundleKitListCreateAPIView.as_view(), name='bundles-kits-list-create'),
]