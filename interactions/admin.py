from django.contrib import admin
from .models import PostLike, Follow, Bookmark
# Register your models here.

class PostLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post_title', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active','created_at')
    search_fields = ('user__full_name', 'post__title')
    ordering = ("-created_at",)
    readonly_fields = ('created_at', 'updated_at')

    def post_title(self, obj):
        return obj.post.title[:50] if len(obj.post.title) > 50 else obj.post.title 
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj = None):
        return False
admin.site.register(PostLike, PostLikeAdmin)


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author_name', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__full_name', 'author__full_name')
    ordering = ("-created_at",)
    readonly_fields = ('created_at',)

    def author_name(self, obj):
        return obj.author.full_name
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj = None):
        return False
admin.site.register(Follow, FollowAdmin)


class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'post_title', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__full_name', 'post__title')
    ordering = ("-created_at",)
    readonly_fields = ('created_at',)

    def post_title(self, obj):
        return obj.post.title[:50] if len(obj.post.title) > 50 else obj.post.title 
    
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj = None):
        return False
admin.site.register(Bookmark, BookmarkAdmin)