from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from posts.models import Post
from .models import PostLike
from .serializers import PostLikeSerializer, UserLikeSerializer
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

# Create your views here.
class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags = ['Interactions'], summary = "To like the post")
    def post(self, request, post_id):
        try:
            post = Post.objects.get(id = post_id)

        except Post.DoesNotExist:
            return Response(
                {'message':'post not found'},
                status = status.HTTP_404_NOT_FOUND)
            
        like_obj, created = PostLike.objects.get_or_create(
                post = post, 
                user = request.user,
                defaults = {'is_active': True}
                )

        if not created:
            like_obj.is_active = not like_obj.is_active     #if like_obj exists then toggle is_active
            like_obj.save()
           
        message = "You liked the post" if like_obj.is_active else "You unliked the post"
        return Response(
                {'message': message},
                status = status.HTTP_200_OK
        )
    
class PostLikeView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(responses = PostLikeSerializer, tags = ['Interactions'], summary = "Total like in the post.")
    def get(self, request, post_id):
        try:
            post = Post.objects.get(id = post_id)
        except Post.DoesNotExist:
            return Response(
                {'message':"Post doesn't exit"},
                status = status.HTTP_404_NOT_FOUND
            )
        active_likes = post.likes.filter(is_active = True)
        count = active_likes.count()
        serializer = PostLikeSerializer(active_likes, many = True)

        return Response(
            {
            'active_likes': count,
            'users': serializer.data
            },
            status = status.HTTP_200_OK)
    
class UserLikeView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses = UserLikeSerializer, tags = ['Interactions'], summary = "To get all likes from the user")
    def get(self, request):
        user = request.user
        mytotallikes = user.mylikes.all()
        serializers = UserLikeSerializer(mytotallikes, many = True)
        like_count = mytotallikes.count()

        return Response(
            {
            'like_count': like_count,
            'posts' : serializers.data,
            },
            status = status.HTTP_200_OK)

            
