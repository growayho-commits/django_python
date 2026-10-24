from django.urls import path
from apps.catalogs.specifications.views.specifications_views import SpecificationsSaveAPIView

app_name = 'specifications'
urlpatterns = [
    path('save/', SpecificationsSaveAPIView.as_view(), name='specifications-save'),
]
