from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from posts.models import Post
from account.models import User
from .models import PostLike, Bookmark, Follow
from .serializers import PostLikeSerializer, UserLikeSerializer, UserBookmarkSerializer,UserFollowerSerializer, UserFollowingSerializer
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
    serializer_classes = UserLikeSerializer

    @extend_schema(responses = UserLikeSerializer, tags = ['Interactions'], summary = "To get user all likes")
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

class PostBookmarkCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags = ['Interactions'], summary = "To bookmark the post")
    def post(self, request, post_id):
        try:
            post = Post.objects.get(id = post_id)
        
        except Post.DoesNotExist:
            return Response(
                {'message':"Post doesn't exists"},
                status = status.HTTP_404_NOT_FOUND
            )
        bookmark_obj = Bookmark.objects.filter(post = post, user = request.user).first()
        if bookmark_obj:
            bookmark_obj.delete()
            return Response(
                {'message':'You unsaved the post'},
                status = status.HTTP_200_OK
            )
        else:
            Bookmark.objects.create(post = post, user = request.user)

        return Response(
            {'message': "You bookmarked/saved the post"},
            status = status.HTTP_201_CREATED
        )
    
class UserBookmarkView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_classes = UserBookmarkSerializer

    @extend_schema(responses = UserBookmarkSerializer, tags = ['Interactions'], summary = "To list user all bookmarks")
    def get(self, request):
        user = request.user
        bookmarked_posts = user.mybookmarks.all()
        serializer = UserBookmarkSerializer(bookmarked_posts, many = True)
        bookmark_count = bookmarked_posts.count()

        return Response(
            {'bookmark_count':bookmark_count,
            'post':serializer.data},
            status = status.HTTP_200_OK)
    
class FollowView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags = ['Interactions'], summary = "To follow the author")
    def post(self, request, author_id):
        try:
            author = User.objects.get(id = author_id)
        except User.DoesNotExist:
            return Response(
                {'message': 'Author doesnot exist'},
                status = status.HTTP_404_NOT_FOUND  
            )
        
        following = Follow.objects.filter(user = request.user, author = author).first()
        if following:
            following.delete()
            return Response(
                {'message':'You unfollowed the author'},
                status = status.HTTP_200_OK
            )
        else:
            Follow.objects.create(user = request.user, author = author)
            return Response(
                {'message':'You followed the author'},
                status = status.HTTP_201_CREATED
            )

class UserFollowersView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses = UserFollowerSerializer, tags = ['Interactions'], summary = "To get user followers")
    def get(self, request):
        author = request.user
        followers = author.followers.all()
        count = followers.count()

        serializer = UserFollowerSerializer(followers, many = True)
        return Response(
            {
                'count':count,
                'followers': serializer.data
            },
            status = status.HTTP_200_OK
        )
    
class UserFollowingView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses = UserFollowingSerializer, tags = ['Interactions'], summary = "To get user followings")
    def get(self, request):
        user = request.user
        following = user.following.all()
        count = following.count()
        serializer = UserFollowingSerializer(following, many = True)
        return Response(
            {'count': count,
             'following': serializer.data}
        )

