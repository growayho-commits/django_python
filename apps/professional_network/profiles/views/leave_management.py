from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from apps.professional_network.profiles.models.availability import ProviderAvailability

@login_required
def update_availability_view(request, profile_id):
    availability = get_object_or_404(ProviderAvailability, profile__id=profile_id, profile__user=request.user)
    if request.method == 'POST':
        availability.is_available = 'is_available' in request.POST
        availability.is_on_leave = 'is_on_leave' in request.POST
        availability.working_hours = request.POST.get('working_hours', availability.working_hours)
        availability.save()
    return redirect('professional_network:profiles:update_schedule', profile_id=profile_id)