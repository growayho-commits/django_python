from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.users.superusers.forms.common_profile_forms import (
    BusinessProfileForm,
    IndividualProfileForm,
    UserAddressForm,
)
from apps.users.superusers.models import BusinessProfile, IndividualProfile, UserAddress
from apps.users.superusers.views.superuser_views import get_user_dashboard_url


@login_required
def common_profile_view(request):
    user = request.user
    individual_profile, _ = IndividualProfile.objects.get_or_create(user=user)
    business_profile = BusinessProfile.objects.filter(user=user).first()
    addresses = UserAddress.objects.filter(user=user).order_by('-is_default', '-created_at')

    individual_form = IndividualProfileForm(instance=individual_profile, prefix='ind')
    business_form = BusinessProfileForm(instance=business_profile, prefix='biz')
    address_form = UserAddressForm(prefix='addr')

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'individual':
            individual_form = IndividualProfileForm(request.POST, instance=individual_profile, prefix='ind')
            if individual_form.is_valid():
                individual_form.save()
                messages.success(request, 'Individual profile updated successfully.')
                return redirect('users:common_profile')

        elif form_type == 'business':
            business_form = BusinessProfileForm(request.POST, instance=business_profile, prefix='biz')
            if business_form.is_valid():
                biz = business_form.save(commit=False)
                biz.user = user
                biz.save()
                messages.success(request, 'Business profile updated successfully.')
                return redirect('users:common_profile')

        elif form_type == 'address':
            address_form = UserAddressForm(request.POST, prefix='addr')
            if address_form.is_valid():
                addr = address_form.save(commit=False)
                addr.user = user
                addr.business_profile = business_profile
                if addr.is_default:
                    UserAddress.objects.filter(user=user, is_default=True).update(is_default=False)
                addr.save()
                messages.success(request, 'Address added successfully.')
                return redirect('users:common_profile')

    return render(request, 'superusers/common_profile.html', {
        'individual_form': individual_form,
        'business_form': business_form,
        'address_form': address_form,
        'addresses': addresses,
        'dashboard_url': get_user_dashboard_url(user),
    })