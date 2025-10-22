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
            'category'
        ]
    
        
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