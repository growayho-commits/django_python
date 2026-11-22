from django.contrib import admin
from .models import MemberProfile

# --- Auto-Generated Model Registrations ---
@admin.register(MemberProfile)
class MemberProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in MemberProfile._meta.fields]
    search_fields = [f.name for f in MemberProfile._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]
