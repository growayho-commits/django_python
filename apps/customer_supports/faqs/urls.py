from django.urls import path
from apps.customer_supports.faqs.views.faq_views import faq_list_view, faq_create_view

urlpatterns = [
    path('', faq_list_view, name='faq_list'),
    path('add/', faq_create_view, name='faq_add'),
]