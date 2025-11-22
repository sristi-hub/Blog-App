from rest_framework import serializers
from .models import PostLike
from account.models import User
from posts.models import Post
from drf_spectacular.utils import extend_schema_field

class PostLikeSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    class Meta:
        model = PostLike
        
        fields = [
            'username',
        ]

    def get_username(self, obj):
        return obj.user.full_name

class UserLikeSerializer(serializers.ModelSerializer):
    post_title = serializers.SerializerMethodField()
    class Meta:
        model = PostLike
        fields = [
            'post_id',
            'post_title'
        ]
    @extend_schema_field(serializers.CharField())
    def get_post_title(self, obj):
        return obj.post.title
