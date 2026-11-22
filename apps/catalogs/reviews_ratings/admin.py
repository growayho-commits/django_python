from django.contrib import admin
from .models import ReviewRatingProfile

# --- Auto-Generated Model Registrations ---
@admin.register(ReviewRatingProfile)
class ReviewRatingProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in ReviewRatingProfile._meta.fields]
    search_fields = [f.name for f in ReviewRatingProfile._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]
