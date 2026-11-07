from django import forms
from apps.customer_supports.live_chats.models.chat_profile import ChatMessageProfile # Adjust if model name differs

class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessageProfile
        fields = ['message']
        widgets = {
            'message': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type your message here...'}),
        }