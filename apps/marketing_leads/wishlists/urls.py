from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.marketing_leads.wishlists.views import WishlistViewSet

router = DefaultRouter()
router.register(r'wishlists', WishlistViewSet, basename='marketing-wishlist')

urlpatterns = [
    path('', include(router.urls)),
]