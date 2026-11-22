from django.urls import path
from . import views

app_name = 'merchant'

urlpatterns = [
    path('', views.overview_view, name='overview'),
    path('overview/', views.overview_view, name='overview'),
    path('catalogs/', views.catalogs_view, name='catalogs'),
    path('bundles/', views.bundles_view, name='bundles'),
    path('orders/', views.orders_view, name='orders'),
    path('logistics/', views.logistics_view, name='logistics'),
    path('finances/', views.finances_view, name='finances'),
    path('profile/', views.profile_view, name='profile'),
]