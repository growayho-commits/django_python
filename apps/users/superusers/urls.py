from django.urls import path
from . import views
from .views import assignment_views, common_profile_views, role_request_views

urlpatterns = [
    path('guest-home/', views.guest_home_view, name='guest_home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('in-account-register/', views.in_account_register_view, name='in_account_register'),
    path('role-dashboard-redirect/', views.role_dashboard_redirect, name='role_dashboard_redirect'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout_view'),

    # Centralized Common Features (All Users)
    path('common-profile/', common_profile_views.common_profile_view, name='common_profile'),
    path('network-tree/', views.network_tree_view, name='network_tree'),

    # Centralized Role Request & Approval
    path('role-request/', role_request_views.submit_role_request_view, name='role_request_view'),
    path('role-request/submit/', role_request_views.submit_role_request_view, name='submit_role_request'),
    path('manage-roles/', role_request_views.manage_roles_view, name='manage_roles'),
    path('manage-roles/<int:pk>/', role_request_views.handle_role_request, name='handle_role_request'),

    # Superuser Assignments
    path('manage-assignments/', assignment_views.manage_assignments_view, name='manage_assignments'),

    path('', views.overview_view, name='overview'),
    path('overview/', views.overview_view, name='overview'),
    path('products/', views.products_view, name='products'),
    path('inventory/', views.inventory_view, name='inventory'),
    path('orders/', views.orders_view, name='orders'),
    path('payouts/', views.payouts_view, name='payouts'),
    path('support/', views.support_view, name='support'),
    path('profile/', views.profile_view, name='profile'),
]