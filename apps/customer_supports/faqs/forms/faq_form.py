from django import forms
from apps.customer_supports.faqs.models.faq_profile import FAQProfile

class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQProfile
        fields = ['question', 'answer', 'is_active']
        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the question...'}),
            'answer': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter detailed answer...'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }