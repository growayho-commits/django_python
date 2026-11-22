from django.urls import path
from apps.users.executives.views import executive_views

app_name = "executives"

urlpatterns = [
    path("dashboard/", executive_views.executive_dashboard, name="dashboard"),
    path("dashboard/", executive_views.executive_dashboard, name="overview"),
    path("executive-dashboard/", executive_views.executive_dashboard, name="executive_dashboard"),
    path("leads/", executive_views.executive_dashboard, name="leads"),
    path("inspections/", executive_views.executive_dashboard, name="inspections"),
    path("onboarding/", executive_views.executive_dashboard, name="onboarding"),
    path("commissions/", executive_views.executive_dashboard, name="commissions"),
    path("reports/", executive_views.executive_dashboard, name="reports"),
    path(
        "profile/",
        executive_views.ExecutiveProfileCreateOrUpdateView.as_view(),
        name="profile",
    ),
]
