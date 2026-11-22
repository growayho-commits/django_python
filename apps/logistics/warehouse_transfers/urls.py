from django.urls import path
from .views.approval_views import approve_transfer_view
from .views.transfer_views import warehouse_transfer_view
from .views.warehouse_transfer_views import FieldInspectionUploadView

app_name = 'warehouse_transfers'

urlpatterns = [
    path('approve-transfer/', approve_transfer_view, name='approve_transfer'),
    path('warehouse-transfer/', warehouse_transfer_view, name='warehouse_transfer'),
    path('field-inspection-upload/', FieldInspectionUploadView.as_view(), name='field_inspection_upload'),
]
