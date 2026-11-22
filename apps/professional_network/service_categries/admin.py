from django.contrib import admin
from .models import ServiceCategory, ServiceAttribute, ServiceListing, ServiceVariationPlan

# --- Auto-Generated Model Registrations ---
@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = [f.name for f in ServiceCategory._meta.fields]
    search_fields = [f.name for f in ServiceCategory._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]

@admin.register(ServiceAttribute)
class ServiceAttributeAdmin(admin.ModelAdmin):
    list_display = [f.name for f in ServiceAttribute._meta.fields]
    search_fields = [f.name for f in ServiceAttribute._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]

@admin.register(ServiceListing)
class ServiceListingAdmin(admin.ModelAdmin):
    list_display = [f.name for f in ServiceListing._meta.fields]
    search_fields = [f.name for f in ServiceListing._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]

@admin.register(ServiceVariationPlan)
class ServiceVariationPlanAdmin(admin.ModelAdmin):
    list_display = [f.name for f in ServiceVariationPlan._meta.fields]
    search_fields = [f.name for f in ServiceVariationPlan._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]
