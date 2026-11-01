from django import forms
from apps.users.guests.models import CoreUser

class GuestRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'royalty-input', 'placeholder': 'Enter Password'})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'royalty-input', 'placeholder': 'Confirm Password'})
    )
    assigned_merchant = forms.ModelChoiceField(
        queryset=CoreUser.objects.filter(role='merchant'),
        required=False,
        empty_label="Select Merchant (Optional)",
        widget=forms.Select(attrs={'class': 'royalty-input'})
    )

    class Meta:
        model = CoreUser
        fields = ['email', 'mobile_number', 'password', 'confirm_password', 'assigned_merchant']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'royalty-input', 'placeholder': 'Enter Email Address'}),
            'mobile_number': forms.TextInput(attrs={'class': 'royalty-input', 'placeholder': 'Enter Mobile Number'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


class GuestLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'royalty-input', 'placeholder': 'Enter Email Address'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'royalty-input', 'placeholder': 'Enter Password'})
    )