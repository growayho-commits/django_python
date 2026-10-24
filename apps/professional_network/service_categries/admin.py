from django.contrib import admin
from apps.professional_network.service_categries.models import (
    ServiceCategory, ServiceAttribute, ServiceListing, ServiceVariationPlan
)

class ServiceAttributeInline(admin.TabularInline):
    model = ServiceAttribute
    extra = 1

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'sac_code', 'google_business_category', 'is_active')
    search_fields = ('name', 'sac_code', 'google_business_category')
    list_filter = ('is_active',)
    inlines = [ServiceAttributeInline]

@admin.register(ServiceAttribute)
class ServiceAttributeAdmin(admin.ModelAdmin):
    list_display = ('title', 'category')
    search_fields = ('title', 'category__name')
    list_filter = ('category',)

class ServiceVariationPlanInline(admin.TabularInline):
    model = ServiceVariationPlan
    extra = 1

@admin.register(ServiceListing)
class ServiceListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('category',)
    inlines = [ServiceVariationPlanInline]

@admin.register(ServiceVariationPlan)
class ServiceVariationPlanAdmin(admin.ModelAdmin):
    list_display = ('plan_name', 'service', 'price', 'estimated_duration')
    search_fields = ('plan_name', 'service__title')
    list_filter = ('price',)