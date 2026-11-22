from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.users.superusers.models.internal_mail import InternalMail
from apps.users.superusers.services.internal_mail_service import InternalMailService
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def inbox_view(request):
    mails = InternalMail.objects.filter(recipient=request.user).order_by('-created_at')
    return render(request, 'superusers/inbox.html', {'mails': mails})

@login_required
def outbox_view(request):
    mails = InternalMail.objects.filter(sender=request.user).order_by('-created_at')
    return render(request, 'superusers/outbox.html', {'mails': mails})

@login_required
def compose_mail_view(request):
    if request.method == 'POST':
        recipient_email = request.POST.get('recipient_email')
        subject = request.POST.get('subject')
        body = request.POST.get('body')
        attachment = request.FILES.get('attachment')
        
        try:
            recipient = User.objects.get(email=recipient_email)
            InternalMailService.send_internal_mail(
                sender=request.user,
                recipient=recipient,
                subject=subject,
                body=body,
                attachment=attachment
            )
            return redirect('users:outbox')
        except User.DoesNotExist:
            # Handle user not found error if needed
            pass
            
    return render(request, 'superusers/compose_mail.html')

@login_required
def mail_detail_view(request, mail_id):
    mail = get_object_or_404(InternalMail, id=mail_id)
    # Check permission
    if mail.recipient == request.user and not mail.is_read:
        mail.is_read = True
        mail.save()
    return render(request, 'superusers/mail_detail.html', {'mail': mail})