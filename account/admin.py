from django.contrib import admin
from .models import User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'contact', 'is_active', 'is_verified', 'role', 'is_staff', 'created_at', 'updated_at')
    search_fields = ('email', 'full_name', 'contact')
    list_filter = ('is_active', 'is_verified', 'role', 'is_staff', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

admin.site.register(User, UserAdmin)