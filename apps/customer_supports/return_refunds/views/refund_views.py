from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.customer_supports.return_refunds.models.refund_profile import ReturnRefundProfile
from apps.customer_supports.return_refunds.forms.refund_form import ReturnRefundForm

@login_required
def refund_list_view(request):
    refunds = ReturnRefundProfile.objects.filter(user=request.user)
    return render(request, 'return_refunds/refund_list.html', {'refunds': refunds})

@login_required
def refund_request_view(request):
    if request.method == 'POST':
        form = ReturnRefundForm(request.POST)
        if form.is_valid():
            refund = form.save(commit=False)
            refund.user = request.user
            refund.save()
            return redirect('refund_list')
    else:
        form = ReturnRefundForm()
    return render(request, 'return_refunds/refund_form.html', {'form': form})