from django.urls import path
from .views.specification_views import SpecificationListCreateAPIView

app_name = 'specifications'

urlpatterns = [
    path('specification-list-create-a-p-i/', SpecificationListCreateAPIView.as_view(), name='specification_list_create_a_p_i'),
]
