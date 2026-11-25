from django.urls import path
from apps.common.views import coverage_scopes_api

app_name = 'common'

urlpatterns = [
    path('coverage-scopes/', coverage_scopes_api, name='coverage_scopes'),
]