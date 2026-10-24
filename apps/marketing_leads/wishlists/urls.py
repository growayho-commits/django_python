from django.urls import path
from apps.catalogs.wishlists.views.wishlists_views import WishlistToggleAPIView

app_name = 'wishlists'
urlpatterns = [
    path('add/', WishlistToggleAPIView.as_view(), name='wishlist-add'),
]
