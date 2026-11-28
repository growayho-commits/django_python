from django import forms
from ..models import RoleUpgradeRequest


class RoleUpgradeRequestForm(forms.ModelForm):
    """
    Form for Members, Sellers, Merchants, and Executives to submit a role upgrade request.
    """
    class Meta:
        model = RoleUpgradeRequest
        fields = ['requested_role', 'business_name', 'gst_number']
        widgets = {
            'requested_role': forms.Select(attrs={
                'class': 'form-select w-full rounded-xl border border-slate-300 px-3 py-2 text-sm',
            }),
            'business_name': forms.TextInput(attrs={
                'class': 'form-control w-full rounded-xl border border-slate-300 px-3 py-2 text-sm',
                'placeholder': 'Business Name (for Seller / Merchant)',
            }),
            'gst_number': forms.TextInput(attrs={
                'class': 'form-control w-full rounded-xl border border-slate-300 px-3 py-2 text-sm',
                'placeholder': 'GST Number (Optional)',
            }),
        }

    def __init__(self, *args, **kwargs):
        excluded_roles = kwargs.pop('excluded_roles', None)
        super().__init__(*args, **kwargs)

        excluded_set = {r.lower() for r in (excluded_roles or [])} | {'superuser'}
        if 'requested_role' in self.fields:
            current_choices = self.fields['requested_role'].choices
            self.fields['requested_role'].choices = [
                (choice_value, choice_label)
                for choice_value, choice_label in current_choices
                if choice_value.lower() not in excluded_set
            ]