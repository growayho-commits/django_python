from django.urls import path
from .views.bundle_kit_views import BundleKitListCreateAPIView

app_name = 'bundles_kits'

urlpatterns = [
    path('bundle-kit-list-create-a-p-i/', BundleKitListCreateAPIView.as_view(), name='bundle_kit_list_create_a_p_i'),
]
