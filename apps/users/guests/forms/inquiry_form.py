# apps/users/guests/forms/inquiry_form.py

from django import forms
from apps.users.guests.models.guest_inquiry import GuestInquiry

class GuestInquiryForm(forms.ModelForm):
    class Meta:
        model = GuestInquiry
        # 🛑 இங்கே மாடலில் உள்ள சரியான புலப் பெயர்களைப் பயன்படுத்த வேண்டும்
        fields = ['full_name', 'email', 'phone_number', 'subject', 'message']
        
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject of your inquiry'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Write your message here...'}),
        }