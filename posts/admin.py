from django.contrib import admin
from .models import Category, Post
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

admin.site.register(Category, CategoryAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'small_content', 'author_name', 'category', 'status', 'created_at', 'updated_at')
    search_fields = ('title', 'author__full_name', 'category')
    list_filter = ('status', 'created_at', 'category')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    def author_name(self, obj):
        return obj.author.full_name

    def small_content(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    

admin.site.register(Post, PostAdmin)