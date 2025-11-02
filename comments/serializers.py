from rest_framework import serializers
from .models import Comment
from account.serializers import UserGetSerializer
from posts.serializers import PostListSerializer
from drf_spectacular.utils import extend_schema_field

class CommentsListSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = [
            'content',
            'user_name',
            'created_at',
            'updated_at'

        ]
    
    @extend_schema_field(serializers.CharField())  #SerializerMethodField is dynamic — DRF doesn’t know what type it returns.
    def get_user_name(self, obj):
        return obj.user.full_name

class CommentCreateSerializer(serializers.Serializer):
    content = serializers.CharField(max_length = 200, trim_whitespace = False)

    def create(self, validated_data):
        user = self.context['user']
        post = self.context['post'] 
        return Comment.objects.create(user = user, post = post, **validated_data)
    
class UserCommentsListSerialzier(serializers.ModelSerializer):
    post = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = [
            'content',
            'post',
            'created_at',
            'updated_at'
        ]

    def get_post(self, obj):
        return obj.post.title