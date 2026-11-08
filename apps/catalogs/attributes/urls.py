from django.urls import path
from apps.catalogs.attributes.views import attribute_views # அல்லது பொருத்தமான வியூ

urlpatterns = [
    path('', attribute_views.attribute_list_view, name='attribute_list'),
]