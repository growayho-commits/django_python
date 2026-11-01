from django.urls import path
from .views import superuser_dashboard, handle_role_request, update_role_requirement
from apps.users.superusers.views.role_views import network_tree_view

urlpatterns = [
    path('dashboard/', superuser_dashboard, name='superuser_dashboard'),
    path('request-action/<int:request_id>/<str:action>/', handle_role_request, name='handle_role_request'),
    path('requirement/update/<int:pk>/', update_role_requirement, name='update_role_requirement'),
    path('network-tree/', network_tree_view, name='network_tree'),
]