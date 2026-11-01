from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from apps.professional_network.enquiries.models.enquiry import SkillEnquiry
from apps.professional_network.ratings.models.review import SkillRating

@login_required
def create_rating_view(request, enquiry_id):
    enquiry = get_object_or_404(SkillEnquiry, id=enquiry_id, sender=request.user)
    if request.method == 'POST':
        stars = request.POST.get('stars')
        feedback = request.POST.get('feedback', '')
        SkillRating.objects.create(
            enquiry=enquiry,
            customer=request.user,
            provider_profile=enquiry.provider_profile,
            stars=int(stars),
            feedback=feedback
        )
        return redirect('professional_network:enquiries:inbox')
    return render(request, 'ratings/review_form.html', {'enquiry': enquiry})