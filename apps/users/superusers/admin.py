from django.contrib import admin
from .models.role_request import RoleUpgradeRequest
from .models.role_requirement import RoleRequirement

@admin.register(RoleUpgradeRequest)
class RoleUpgradeRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'requested_role', 'status', 'created_at')
    search_fields = ('user__email', 'requested_role', 'status')
    list_filter = ('status', 'requested_role', 'created_at')

@admin.register(RoleRequirement)
class RoleRequirementAdmin(admin.ModelAdmin):
    list_display = ('id', 'role_name')
    search_fields = ('role_name',)