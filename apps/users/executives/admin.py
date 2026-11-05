from django.contrib import admin
from .models.executive_profile import ExecutiveProfile

@admin.register(ExecutiveProfile)
class ExecutiveAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    search_fields = ('user__email',)
    list_filter = ('created_at',)