"""
Core URL Configuration for the project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/stable/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # ------------------------------------------------------------------
    # 1. முகப்புப் பக்க ரூட் (Root URL Mapping)
    # ------------------------------------------------------------------
    # சூப்பர்யூசர்ஸ் ஆப் மூலம் அனைத்து ஹோம் மற்றும் ஆதெண்டிகேஷன் இயக்கப்படுகிறது
    path('', include('apps.users.superusers.urls')),

    # ------------------------------------------------------------------
    # 2. அட்மின் பேனல் (Django Admin Interface)
    # ------------------------------------------------------------------
    path('admin/', admin.site.urls),

    # ------------------------------------------------------------------
    # 3. ஆப் அமைப்புகள் (App Level URL Routing with Namespaces)
    # ------------------------------------------------------------------
    # Catalogs ஆப் (தயாரிப்புப் பட்டியல்கள் மற்றும் இன்வென்டரி விவரங்கள்)
    path('api/v1/catalogs/', include(('apps.catalogs.core_catalogs.urls', 'core_catalogs'), namespace='core_catalogs')),
    
    # Users ஆப் (மற்றும் அதன் உட்பிரிவுகள்: members, merchant, executives, sellers)
    path('api/v1/users/', include('apps.users.urls')),

    # Professional Network ஆப் (தொழில்முறை சேவை வழங்குநர்களின் நெட்வொர்க்)
    path('api/v1/professional-network/', include('apps.professional_network.urls')),

    # ------------------------------------------------------------------
    # 4. இதர மாடியூல் ரூட்டுகள் (Optional Routes)
    # ------------------------------------------------------------------
    path('api/v1/marketing/', include('apps.marketing_leads.urls')),
    path('api/v1/support/', include('apps.customer_supports.urls')),
    
    # தற்காலிகமாக கமெண்ட் செய்யப்பட்டுள்ளவை (தேவைப்படும்போது அன்-கமெண்ட் செய்து கொள்ளலாம்)
    # path('api/v1/finances/', include('apps.finances.urls')),
    # path('api/v1/logistics/', include('apps.logistics.urls')),
    # path('api/v1/systems/', include('apps.systems.urls')),
]