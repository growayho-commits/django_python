from django.shortcuts import render, redirect
from apps.professional_network.service_categries.models import ServiceCategory
from apps.users.guests.forms.inquiry_form import GuestInquiryForm

from django.shortcuts import render

def guest_home_view(request):
    """
    HYBRID MARKETPLACE பிளாட்ஃபார்மின் முகப்புப் பக்கத்தை (Home Page) காண்பிக்கிறது.
    """
    return render(request, 'guests/guest_home.html')
