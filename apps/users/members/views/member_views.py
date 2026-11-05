from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator

@login_required
def member_dashboard_view(request):
    """
    மெம்பர் டேஷ்போர்டு வியூ
    """
    return render(request, 'members/dashboard.html')

@method_decorator(login_required, name='dispatch')
class MemberProfileCreateOrUpdateView(TemplateView):
    """
    மெம்பர் சுயவிவரத்தை உருவாக்கும் அல்லது புதுப்பிக்கும் வியூ
    """
    template_name = 'members/member_profile.html'