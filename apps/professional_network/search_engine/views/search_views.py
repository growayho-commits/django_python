from django.db.models import Q
from django.shortcuts import render
from apps.professional_network.profiles.models.skill_profile import ProfessionalProfile
from apps.professional_network.search_engine.models.search_log import SearchLog

def directory_home_view(request):
    profiles = ProfessionalProfile.objects.filter(availability__is_available=True, availability__is_on_leave=False)[:10]
    return render(request, 'search_engine/directory_home.html', {'profiles': profiles})

def professional_search_view(request):
    query = request.GET.get('q', '')
    location = request.GET.get('location', '')

    if query:
        SearchLog.objects.create(user=request.user if request.user.is_authenticated else None, query_text=query, location_text=location)

    profiles = ProfessionalProfile.objects.filter(
        availability__is_available=True,
        availability__is_on_leave=False
    )

    if query:
        profiles = profiles.filter(
            Q(skill_title__icontains=query) |
            Q(description__icontains=query) |
            Q(hsn_service_code__icontains=query)
        )

    if location:
        profiles = profiles.filter(
            Q(city__icontains=location) |
            Q(pincode__icontains=location)
        )

    context = {
        'profiles': profiles,
        'query': query,
        'location': location,
    }
    return render(request, 'search_engine/search_results.html', context)