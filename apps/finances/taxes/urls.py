from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.tax_views import TaxViewSet

router = DefaultRouter()
router.register(r'taxes', TaxViewSet, basename='taxes')

urlpatterns = [
    path('', include(router.urls)),
]