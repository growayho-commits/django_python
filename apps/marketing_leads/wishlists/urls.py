from django.urls import path
from .views.wishlist_views import WishlistViewSet

app_name = 'wishlists'

urlpatterns = [
    path('wishlist/', WishlistViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'}), name='wishlist'),
]
