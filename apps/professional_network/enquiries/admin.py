from django.contrib import admin
from .models import SkillEnquiry

# --- Auto-Generated Model Registrations ---
@admin.register(SkillEnquiry)
class SkillEnquiryAdmin(admin.ModelAdmin):
    list_display = [f.name for f in SkillEnquiry._meta.fields]
    search_fields = [f.name for f in SkillEnquiry._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]
