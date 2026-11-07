from django import forms
from apps.customer_supports.return_refunds.models.refund_profile import ReturnRefundProfile

class ReturnRefundForm(forms.ModelForm):
    class Meta:
        model = ReturnRefundProfile
        fields = ['order', 'reason', 'description', 'refund_amount']
        widgets = {
            'order': forms.Select(attrs={'class': 'form-select'}),
            'reason': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Provide details about the return/refund...'}),
            'refund_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
        }