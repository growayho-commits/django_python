from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.customer_supports.faqs.models.faq_profile import FAQProfile
from apps.customer_supports.faqs.forms.faq_form import FAQForm

@login_required
def faq_list_view(request):
    """
    List all FAQ entries.
    Template location: apps/customer_supports/faqs/templates/faqs/faq_list.html
    """
    faqs = FAQProfile.objects.all()
    return render(request, 'faqs/faq_list.html', {'faqs': faqs})

@login_required
def faq_create_view(request):
    """
    Handle creation of new FAQ items.
    Template location: apps/customer_supports/faqs/templates/faqs/faq_form.html
    """
    if request.method == 'POST':
        form = FAQForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('faq_list')
    else:
        form = FAQForm()
    
    return render(request, 'faqs/faq_form.html', {'form': form})