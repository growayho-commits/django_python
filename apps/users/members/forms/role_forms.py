from django import forms
from apps.users.superusers.models import RoleUpgradeRequest

class RoleUpgradeRequestForm(forms.ModelForm):
    """
    Form for users (Members, Sellers, Merchants, Executives) to submit a new role request.
    """
    class Meta:
        model = RoleUpgradeRequest
        fields = ['requested_role']
        widgets = {
            'requested_role': forms.Select(attrs={'class': 'form-select'}),
        }