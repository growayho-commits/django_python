from django.urls import path
from . import views

app_name = 'sellers'

urlpatterns = [
    path('', views.overview_view, name='overview'),
    path('overview/', views.overview_view, name='overview'),
    path('products/', views.products_view, name='products'),
    path('inventory/', views.inventory_view, name='inventory'),
    path('orders/', views.orders_view, name='orders'),
    path('payouts/', views.payouts_view, name='payouts'),
    path('support/', views.support_view, name='support'),
    path('profile/', views.profile_view, name='profile'),
]