from django.urls import path
from apps.professional_network.enquiries.views import send_enquiry_view, inbox_view

app_name = 'enquiries'

urlpatterns = [
    path('send/<int:profile_id>/', send_enquiry_view, name='send_enquiry'),
    path('inbox/', inbox_view, name='inbox'),
]