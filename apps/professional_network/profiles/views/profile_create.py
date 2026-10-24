from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.professional_network.profiles.models.skill_profile import ProfessionalProfile
from apps.professional_network.profiles.models.availability import ProviderAvailability

@login_required
def create_profile_view(request):
    if request.method == 'POST':
        skill_title = request.POST.get('skill_title')
        hsn_service_code = request.POST.get('hsn_service_code')
        description = request.POST.get('description')
        experience_years = request.POST.get('experience_years', 0)
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        working_hours = request.POST.get('working_hours', '9:00 AM - 6:00 PM')

        profile = ProfessionalProfile.objects.create(
            user=request.user,
            skill_title=skill_title,
            hsn_service_code=hsn_service_code,
            description=description,
            experience_years=experience_years,
            city=city,
            pincode=pincode
        )
        ProviderAvailability.objects.create(
            profile=profile,
            working_hours=working_hours,
            is_available=True,
            is_on_leave=False
        )
        return redirect('professional_network:search_engine:search_results')
    return render(request, 'profiles/create_skill.html')