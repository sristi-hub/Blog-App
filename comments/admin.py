from django.contrib import admin
from .models import Comment
# Register your models here.

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'short_content', 'post_title', 'parent_full_name', 'parent_content', 'created_at', 'updated_at', 'status')
    search_fields = ('user__full_name', 'post__title', 'content')
    list_filter = ('status', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    def short_content(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content

    def post_title(self, obj):
        return obj.post.title

    def parent_full_name(self, obj):
        return obj.parent.user.full_name if obj.parent else None
    
    def parent_content(self,obj):
        return obj.parent.content[:50] if obj.parent else None
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj = None):
        return False

admin.site.register(Comment, CommentAdmin)