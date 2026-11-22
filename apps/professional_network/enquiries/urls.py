from django.urls import path
from .views.inbox_views import inbox_view
from .views.send_enquiry import send_enquiry_view

app_name = 'enquiries'

urlpatterns = [
    path('inbox/', inbox_view, name='inbox'),
    path('send-enquiry/', send_enquiry_view, name='send_enquiry'),
]
