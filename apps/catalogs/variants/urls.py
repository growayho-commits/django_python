from django.urls import path
from .views.variant_views import VariantListCreateAPIView

app_name = 'variants'

urlpatterns = [
    path('variant-list-create-a-p-i/', VariantListCreateAPIView.as_view(), name='variant_list_create_a_p_i'),
]
