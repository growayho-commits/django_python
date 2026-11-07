from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.customer_supports.helpdesk_tickets.models.ticket_profile import HelpdeskTicket
from apps.customer_supports.helpdesk_tickets.forms.ticket_form import HelpdeskTicketForm

@login_required
def ticket_list_view(request):
    tickets = HelpdeskTicket.objects.filter(user=request.user)
    return render(request, 'helpdesk_tickets/ticket_list.html', {'tickets': tickets})

@login_required
def ticket_create_view(request):
    if request.method == 'POST':
        form = HelpdeskTicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('ticket_list')
    else:
        form = HelpdeskTicketForm()
    return render(request, 'helpdesk_tickets/ticket_form.html', {'form': form})