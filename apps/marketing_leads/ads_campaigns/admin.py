from django.contrib import admin
from .models import AdsCampaignProfile

# --- Auto-Generated Model Registrations ---
@admin.register(AdsCampaignProfile)
class AdsCampaignProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in AdsCampaignProfile._meta.fields]
    search_fields = [f.name for f in AdsCampaignProfile._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]
