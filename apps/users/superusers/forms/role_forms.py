from django import forms
from ..models import RoleRequirement

class RoleRequirementForm(forms.ModelForm):
    class Meta:
        model = RoleRequirement
        fields = ['role_name', 'require_basic_profile', 'require_business_profile', 'require_gst']
        widgets = {
            'role_name': forms.Select(attrs={'class': 'form-select'}),
            'require_basic_profile': forms.Select(attrs={'class': 'form-select'}),
            'require_business_profile': forms.Select(attrs={'class': 'form-select'}),
            'require_gst': forms.Select(attrs={'class': 'form-select'}),
        }