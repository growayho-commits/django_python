from django.urls import path
from .views.faq_views import faq_list_view, faq_create_view

app_name = 'faqs'

urlpatterns = [
    path('faq-list/', faq_list_view, name='faq_list'),
    path('faq-create/', faq_create_view, name='faq_create'),
]
