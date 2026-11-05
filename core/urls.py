"""
Core URL Configuration for the project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/stable/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    # ------------------------------------------------------------------
    # 1. முகப்புப் பக்க ரெடிரெக்ட் (Root URL Redirect)
    # ------------------------------------------------------------------
    # பயனர் தளம்/டொமைனின் முதன்மைப் பக்கத்திற்கு (http://127.0.0.1:8000/) வரும்போது 
    # நேரடியாக guests லாகின் பக்கத்திற்கு (guests:login) அனுப்பி வைக்கப்படும்.
    path('', RedirectView.as_view(pattern_name='guests:login', permanent=False), name='root_redirect'),

    # ------------------------------------------------------------------
    # 2. அட்மின் பேனல் (Django Admin Interface)
    # ------------------------------------------------------------------
    path('admin/', admin.site.urls),

    # ------------------------------------------------------------------
    # 3. ஆப் அமைப்புகள் (App Level URL Routing with Namespaces)
    # ------------------------------------------------------------------
    # Catalogs ஆப்
    path('api/v1/catalogs/', include('apps.catalogs.urls', namespace='catalogs')),

    # Users ஆப் (மற்றும் அதன் உட்பிரிவுகள்: guests, members, merchant, executives, sellers, superusers)
    path('api/v1/users/', include('apps.users.urls')),

    # Professional Network ஆப்
    path('api/professional-network/', include('apps.professional_network.urls')),

    # ------------------------------------------------------------------
    # 4. எதிர்கால பயன்பாட்டிற்கான ஆப் மாடியூல்கள் (Optional / Commented Routes)
    # தேவைப்படும் போது இவற்றை அன்-கமெண்ட் (Uncomment) செய்து பயன்படுத்தலாம்.
    # ------------------------------------------------------------------
    # path('api/v1/support/', include('apps.customer_supports.urls')),
    # path('api/v1/finances/', include('apps.finances.urls')),
    # path('api/v1/logistics/', include('apps.logistics.urls')),
    # path('api/v1/marketing/', include('apps.marketing_leads.urls')),
    # path('api/v1/systems/', include('apps.systems.urls')),
]