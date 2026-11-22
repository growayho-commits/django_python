from django import forms
from apps.users.superusers.models import IndividualProfile, BusinessProfile, UserAddress


class IndividualProfileForm(forms.ModelForm):
    class Meta:
        model = IndividualProfile
        fields = [
            'first_name', 'last_name', 'phone_number',
            'date_of_birth', 'gender', 'address', 'city', 'state', 'pincode',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'w-full rounded-xl border border-slate-300 px-3 py-2 text-sm'}),
            'address': forms.Textarea(attrs={'rows': 2, 'class': 'w-full rounded-xl border border-slate-300 px-3 py-2 text-sm'}),
        }


class BusinessProfileForm(forms.ModelForm):
    class Meta:
        model = BusinessProfile
        fields = [
            'company_name', 'business_type', 'gst_number', 'pan_number',
            'business_address', 'business_city', 'business_state', 'business_pincode',
            'business_email', 'business_phone',
        ]
        widgets = {
            'business_address': forms.Textarea(attrs={'rows': 2, 'class': 'w-full rounded-xl border border-slate-300 px-3 py-2 text-sm'}),
        }


class UserAddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = [
            'address_type', 'address_title', 'contact_person_name', 'phone_number',
            'address_line1', 'address_line2', 'city', 'state', 'pincode',
            'gstin_number', 'is_default',
        ]
        widgets = {
            'address_line1': forms.Textarea(attrs={'rows': 2, 'class': 'w-full rounded-xl border border-slate-300 px-3 py-2 text-sm'}),
            'address_line2': forms.Textarea(attrs={'rows': 2, 'class': 'w-full rounded-xl border border-slate-300 px-3 py-2 text-sm'}),
        }