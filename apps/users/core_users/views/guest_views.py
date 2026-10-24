from django.shortcuts import render, redirect
from apps.professional_network.service_categries.models import ServiceCategory
from apps.users.core_users.forms.inquiry_form import GuestInquiryForm

def guest_home_view(request):
    parent_categories = ServiceCategory.objects.filter(parent__isnull=True, is_active=True)
    all_categories = ServiceCategory.objects.filter(is_active=True)
    
    if request.method == 'POST':
        form = GuestInquiryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('guest_home')
    else:
        form = GuestInquiryForm()

    context = {
        'parent_categories': parent_categories,
        'all_categories': all_categories,
        'form': form,
    }
    return render(request, 'core_users/guest_home.html', context)
