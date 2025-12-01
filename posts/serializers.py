from rest_framework import serializers
from .models import Post, Category
from drf_spectacular.utils import extend_schema_field

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'description'
        ]
        
class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'category',
            'status'
        ]

    def validate_status(self, value):
        user = self.context['request'].user

        #User can only change status to either 'draft' or 'pending'
        if user.role == 'user':
            allowed = ['draft', 'pending']
            if value not in allowed:
                raise serializers.ValidationError(
                f"Users can only set status to {allowed}" 
                )

        return value   
    
        
class PostListSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'content',
            'author',
            'created_at',
            'category',
            'status'
        ]

    @extend_schema_field(serializers.CharField())
    def get_author(self, obj):
        return (obj.author.full_name)
    
    @extend_schema_field(serializers.CharField())
    def get_category(self, obj):
        return (obj.category.name)

    

class EmptySerializer(serializers.Serializer):
    pass

class ModeratorPostStatusUpdateSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['status']

    def validate_status(self, value):
        allowed = ['approved', 'rejected', 'published']        
        if value not in allowed:
            raise serializers.ValidationError(
            f"Moderator can only set status to {allowed}")

        return value