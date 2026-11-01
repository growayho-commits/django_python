from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.professional_network.enquiries.models.enquiry import SkillEnquiry

@login_required
def inbox_view(request):
    sent = SkillEnquiry.objects.filter(sender=request.user)
    received = SkillEnquiry.objects.filter(provider_profile__user=request.user)
    context = {
        'sent_enquiries': sent,
        'received_enquiries': received,
    }
    return render(request, 'enquiries/inbox.html', context)