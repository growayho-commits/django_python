# E:\django_python\apps\users\superusers\admin.py

from django.contrib import admin
from .models import RoleUpgradeRequest

# --- Auto-Generated Model Registrations ---
@admin.register(RoleUpgradeRequest)
class RoleUpgradeRequestAdmin(admin.ModelAdmin):
    list_display = [f.name for f in RoleUpgradeRequest._meta.fields]
    search_fields = [f.name for f in RoleUpgradeRequest._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]