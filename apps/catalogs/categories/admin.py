from django.contrib import admin
from .models import CategoryProfile

# --- Auto-Generated Model Registrations ---
@admin.register(CategoryProfile)
class CategoryProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in CategoryProfile._meta.fields]
    search_fields = [f.name for f in CategoryProfile._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]
