from django.urls import path
from .views.category_views import CategoryListCreateAPIView

app_name = 'categories'

urlpatterns = [
    path('category-list-create-a-p-i/', CategoryListCreateAPIView.as_view(), name='category_list_create_a_p_i'),
]
