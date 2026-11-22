"""
Tier-1 Core Main URL Configuration â€” 9-Tier Enterprise Architecture
Auto-synchronized by cli/create_urls.py (Namespaced & Root Handled)
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    # Direct Root mapping to Guest Home page view
    path('', RedirectView.as_view(pattern_name='users:guest_home', permanent=False), name='home'),
    # Django Admin Panel
    path('admin/', admin.site.urls),
    # --- Tier-3: Group App API Routers ---
    path('api/v1/catalogs/', include(('apps.catalogs.urls', 'catalogs'))),
    path('api/v1/customer_supports/', include(('apps.customer_supports.urls', 'customer_supports'))),
    path('api/v1/finances/', include(('apps.finances.urls', 'finances'))),
    path('api/v1/logistics/', include(('apps.logistics.urls', 'logistics'))),
    path('api/v1/marketing_leads/', include(('apps.marketing_leads.urls', 'marketing_leads'))),
    path('api/v1/professional_network/', include(('apps.professional_network.urls', 'professional_network'))),
    path('api/v1/systems/', include(('apps.systems.urls', 'systems'))),
    path('api/v1/users/', include(('apps.users.urls', 'users'))),
]
