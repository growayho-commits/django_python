from django.urls import path
from apps.customer_supports.helpdesk_tickets.views.ticket_views import ticket_list_view, ticket_create_view

urlpatterns = [
    path('', ticket_list_view, name='ticket_list'),
    path('create/', ticket_create_view, name='ticket_create'),
]