from django.contrib import admin
from .models import BundleKitProfile

# --- Auto-Generated Model Registrations ---
@admin.register(BundleKitProfile)
class BundleKitProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in BundleKitProfile._meta.fields]
    search_fields = [f.name for f in BundleKitProfile._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]
