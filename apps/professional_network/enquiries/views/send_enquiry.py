from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from apps.professional_network.profiles.models.skill_profile import ProfessionalProfile
from apps.professional_network.enquiries.models.enquiry import SkillEnquiry

@login_required
def send_enquiry_view(request, profile_id):
    profile = get_object_or_404(ProfessionalProfile, id=profile_id)
    if request.method == 'POST':
        message = request.POST.get('message')
        SkillEnquiry.objects.create(
            sender=request.user,
            provider_profile=profile,
            message=message
        )
        return redirect('professional_network:enquiries:inbox')
    return render(request, 'enquiries/send_modal.html', {'profile': profile})