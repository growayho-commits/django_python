from django.urls import path
from apps.users.members.views import member_views

app_name = 'members'

urlpatterns = [
    path('dashboard/', member_views.member_dashboard_view, name='dashboard'),
    path('catalogs/', member_views.member_catalogs_view, name='catalogs'),
    path('catalogs/add-to-cart/<int:product_id>/', member_views.add_to_cart_view, name='add_to_cart'),
    path('catalogs/toggle-wishlist/<int:product_id>/', member_views.toggle_wishlist_view, name='toggle_wishlist'),
    path('orders/', member_views.member_orders_view, name='orders'),
    path('profile/', member_views.member_profile_view, name='profile'),
    path('requests/', member_views.member_requests_view, name='requests'),
    path('services/', member_views.member_services_view, name='services'),
]