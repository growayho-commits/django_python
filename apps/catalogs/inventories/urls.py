from django.urls import path
from .views.inventory_views import InventoryListCreateAPIView

app_name = 'inventories'

urlpatterns = [
    path('inventory-list-create-a-p-i/', InventoryListCreateAPIView.as_view(), name='inventory_list_create_a_p_i'),
]
