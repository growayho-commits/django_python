from django.contrib import admin
from .models.member_profile import MemberProfile

@admin.register(MemberProfile)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    search_fields = ('user__email',)
    list_filter = ('created_at',)