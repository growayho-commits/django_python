from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [

    path('', include('apps.users.core_users.urls')),
     
    path('admin/', admin.site.urls),
    path('api/v1/catalogs/', include('apps.catalogs.urls', namespace='catalogs')),
    path('api/v1/users/', include('apps.users.core_users.urls')),
    #path('api/v1/support/', include('apps.customer_supports.urls')), # தேவைப்பட்டால் சப்-ஆப் வாரியாகவும் பிரிக்கலாம்
    #path('api/v1/finances/', include('apps.finances.urls')),
    #path('api/v1/logistics/', include('apps.logistics.urls')),
    #path('api/v1/marketing/', include('apps.marketing_leads.urls')),
    #path('api/v1/systems/', include('apps.systems.urls')),
    path('api/professional-network/', include('apps.professional_network.urls')),

]