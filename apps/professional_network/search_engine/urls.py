from django.urls import path
from .views.search_views import directory_home_view, professional_search_view

app_name = 'search_engine'

urlpatterns = [
    path('directory-home/', directory_home_view, name='directory_home'),
    path('professional-search/', professional_search_view, name='professional_search'),
]
