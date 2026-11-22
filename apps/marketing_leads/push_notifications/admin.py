from django.contrib import admin
from .models import PushNotificationProfile

# --- Auto-Generated Model Registrations ---
@admin.register(PushNotificationProfile)
class PushNotificationProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in PushNotificationProfile._meta.fields]
    search_fields = [f.name for f in PushNotificationProfile._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]
