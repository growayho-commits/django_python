from django.contrib import admin
from .models import SkillRating

# --- Auto-Generated Model Registrations ---
@admin.register(SkillRating)
class SkillRatingAdmin(admin.ModelAdmin):
    list_display = [f.name for f in SkillRating._meta.fields]
    search_fields = [f.name for f in SkillRating._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]
