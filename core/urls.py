"""
Core URL Configuration for the project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/stable/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include

# 1. விருந்தினர் முகப்புப் பக்க வியூவை (guest_home_view) சரியாக இம்போர்ட் செய்தல்
from apps.users.guests.views.core_users_views import guest_home_view

urlpatterns = [
    # ------------------------------------------------------------------
    # 1. முகப்புப் பக்க ரூட் (Root URL Mapping)
    # ------------------------------------------------------------------
    # பயனர் தளம்/டொமைனின் முதன்மைப் பக்கத்திற்கு (http://127.0.0.1:8000/) வரும்போது 
    # நேரடியாக உங்களது guest_home.html முகப்புப் பக்கம் திறக்கப்படும்.
    path('', guest_home_view, name='guest_home'),

    # ------------------------------------------------------------------
    # 2. அட்மின் பேனல் (Django Admin Interface)
    # ------------------------------------------------------------------
    path('admin/', admin.site.urls),

    # ------------------------------------------------------------------
    # 3. ஆப் அமைப்புகள் (App Level URL Routing with Namespaces)
    # ------------------------------------------------------------------
    # Catalogs ஆப் (தயாரிப்புப் பட்டியல்கள் மற்றும் இன்வென்டரி விவரங்கள்)
    path('api/v1/catalogs/', include(('apps.catalogs.core_catalogs.urls', 'core_catalogs'), namespace='core_catalogs')),
    
    # Users ஆப் (மற்றும் அதன் உட்பிரிவுகள்: guests, members, merchant, executives, sellers, superusers)
    path('api/v1/users/', include('apps.users.urls')),

    # Professional Network ஆப் (தொழில்முறை சேவை வழங்குநர்களின் நெட்வொர்க்)
    path('api/v1/professional-network/', include('apps.professional_network.urls')),

    # ------------------------------------------------------------------
    # 4. எதிர்கால பயன்பாட்டிற்கான மற்றும் மாடியூல் ரூட்டுகள் (Optional Routes)
    # ------------------------------------------------------------------
    # மார்க்கெட்டிங் மற்றும் லீட்ஸ் மாடியூல்
    path('api/v1/marketing/', include('apps.marketing_leads.urls')),
    
    # தேவையெனில் மற்ற மாடியூல்களை இங்கே அன்-கமெண்ட் செய்து இணைத்துக் கொள்ளலாம்:
    path('api/v1/support/', include('apps.customer_supports.urls')),
    # path('api/v1/finances/', include('apps.finances.urls')),
    # path('api/v1/logistics/', include('apps.logistics.urls')),
    # path('api/v1/systems/', include('apps.systems.urls')),
]
