from django import forms
from apps.customer_supports.helpdesk_tickets.models.ticket_profile import HelpdeskTicket

class HelpdeskTicketForm(forms.ModelForm):
    class Meta:
        model = HelpdeskTicket
        fields = ['subject', 'description', 'priority', 'status']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ticket Subject...'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Describe your issue...'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }