from django.db import models
from django.conf import settings

class InternalMail(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_mails')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_mails')
    subject = models.CharField(max_length=255)
    body = models.TextField()
    attachment = models.FileField(upload_to='mail_attachments/', blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mail from {self.sender.email} to {self.recipient.email}: {self.subject}"