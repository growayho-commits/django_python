from apps.users.superusers.models.internal_mail import InternalMail

class InternalMailService:
    @staticmethod
    def send_internal_mail(sender, recipient, subject, body, attachment=None):
        """
        Creates and sends an internal message/mail with text and optional attachment.
        """
        mail = InternalMail.objects.create(
            sender=sender,
            recipient=recipient,
            subject=subject,
            body=body,
            attachment=attachment
        )
        return mail