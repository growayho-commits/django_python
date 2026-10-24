from django.urls import path
from apps.catalogs.inventories.views.inventory_views import InventorySyncAPIView

app_name = 'inventories'

urlpatterns = [
    path('sync/', InventorySyncAPIView.as_view(), name='inventory-sync'),
]