from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def attribute_list_view(request):
    return render(request, 'catalogs/attributes/attribute_list.html')