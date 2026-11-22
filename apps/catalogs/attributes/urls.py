from django.urls import path
from .views.attribute_views import AttributeListCreateAPIView

app_name = 'attributes'

urlpatterns = [
    path('attribute-list-create-a-p-i/', AttributeListCreateAPIView.as_view(), name='attribute_list_create_a_p_i'),
]
