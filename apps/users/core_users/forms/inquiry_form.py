from django import forms
from apps.users.core_users.models.guest_inquiry import GuestInquiry

class GuestInquiryForm(forms.ModelForm):
    class Meta:
        model = GuestInquiry
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'உங்கள் பெயர்'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'உங்கள் மின்னஞ்சல்'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'தொலைபேசி எண்'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'உங்கள் சேவைத் தேவைகள்...', 'rows': 3}),
        }
