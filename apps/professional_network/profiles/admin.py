from django.contrib import admin
from .models import ProviderAvailability, ProfessionalProfile, ProfessionalMedia, ProfessionalStory, ProfessionalEvent

# --- Auto-Generated Model Registrations ---
@admin.register(ProviderAvailability)
class ProviderAvailabilityAdmin(admin.ModelAdmin):
    list_display = [f.name for f in ProviderAvailability._meta.fields]
    search_fields = [f.name for f in ProviderAvailability._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]

@admin.register(ProfessionalProfile)
class ProfessionalProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in ProfessionalProfile._meta.fields]
    search_fields = [f.name for f in ProfessionalProfile._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]

@admin.register(ProfessionalMedia)
class ProfessionalMediaAdmin(admin.ModelAdmin):
    list_display = [f.name for f in ProfessionalMedia._meta.fields]
    search_fields = [f.name for f in ProfessionalMedia._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]

@admin.register(ProfessionalStory)
class ProfessionalStoryAdmin(admin.ModelAdmin):
    list_display = [f.name for f in ProfessionalStory._meta.fields]
    search_fields = [f.name for f in ProfessionalStory._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]

@admin.register(ProfessionalEvent)
class ProfessionalEventAdmin(admin.ModelAdmin):
    list_display = [f.name for f in ProfessionalEvent._meta.fields]
    search_fields = [f.name for f in ProfessionalEvent._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]
