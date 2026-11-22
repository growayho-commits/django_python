from django.urls import path
from .views.catalog_wishlist_views import CatalogWishlistListCreateAPIView

app_name = 'catalog_wishlist'

urlpatterns = [
    path('list-create-a-p-i/', CatalogWishlistListCreateAPIView.as_view(), name='list_create_a_p_i'),
]
