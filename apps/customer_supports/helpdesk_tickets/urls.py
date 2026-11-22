from django.urls import path
from .views.ticket_views import ticket_list_view, ticket_create_view

app_name = 'helpdesk_tickets'

urlpatterns = [
    path('ticket-list/', ticket_list_view, name='ticket_list'),
    path('ticket-create/', ticket_create_view, name='ticket_create'),
]
