from django.urls import path
from .views.audit_views import AuditLogViewSet

app_name = 'audits'

urlpatterns = [
    path('audit-log/', AuditLogViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'}), name='audit_log'),
]
