from rest_framework import serializers
from .models import Comment
from account.serializers import UserGetSerializer
from posts.serializers import PostListSerializer
from drf_spectacular.utils import extend_schema_field

class CommentReplySerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = [
            'content',
            'user_name',
            'created_at',
            'updated_at',
        ]

    @extend_schema_field(serializers.CharField())
    def get_user_name(self, obj):
        return obj.user.full_name

class CommentsListSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    replies = CommentReplySerializer(many = True)
    class Meta:
        model = Comment
        fields = [
            'id',
            'content',
            'user_name',
            'created_at',
            'updated_at',
            'replies',

        ]
    
    @extend_schema_field(serializers.CharField())  #SerializerMethodField is dynamic — DRF doesn’t know what type it returns.
    def get_user_name(self, obj):
        return obj.user.full_name

class CommentCreateSerializer(serializers.Serializer):
    content = serializers.CharField(max_length = 200, trim_whitespace = False)
    parent = serializers.IntegerField(required = False)


    def create(self, validated_data):
        user = self.context['user']
        post = self.context['post'] 
        parent_id = validated_data.pop("parent", None)
        parent = None
        if parent_id is not None:
            try:
                parent = Comment.objects.get(id = parent_id, post = post)
            except:
                raise serializers.ValidationError({'parent':'Invalid comment Id'})
            
        return Comment.objects.create(
            user = user, 
            post = post, 
            parent = parent,
            **validated_data)
    
    
        

    
class UserCommentsListSerialzier(serializers.ModelSerializer):
    post = serializers.SerializerMethodField()
    parent_comment = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = [
            'content',
            'post',
            'created_at',
            'updated_at',
            'parent_comment',
        ]

    @extend_schema_field(serializers.CharField())
    def get_post(self, obj):
        return obj.post.title
    
    @extend_schema_field({
        'type': 'object',
        'properties': {
            'id': {'type': 'integer'},
            'content': {'type': 'string'}
        },
        'nullable': True
    })
    def get_parent_comment(self, obj):
        if obj.parent:
            return{
                'id':obj.parent.id,
                'content':obj.parent.content
            }
        return None
    