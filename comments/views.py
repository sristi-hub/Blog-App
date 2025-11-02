from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from posts.models import Post
from .models import Comment
from .serializers import CommentCreateSerializer, CommentsListSerializer, UserCommentsListSerialzier
from drf_spectacular.utils import extend_schema
# Create your views here.


class CommentCreateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentCreateSerializer

    @extend_schema(request = CommentCreateSerializer, tags = ['Comments'], summary = 'Create a comment')
    def post(self, request, post_id):
        post = Post.objects.get(id = post_id)
        serializer = CommentCreateSerializer(data = request.data, context = {
            'user' : request.user,
            'post' : post
        })
        if serializer.is_valid():
            serializer.save()    
            return Response({'message':'Comment is sent'}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
class CommentsListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentsListSerializer

    @extend_schema(responses = CommentsListSerializer, tags = ['Comments'], summary = 'List all comments of a post')
    def get(self, request, post_id):
        comments = Comment.objects.filter(post_id = post_id)
        serializer = CommentsListSerializer(comments, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
class UserCommentsListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserCommentsListSerialzier

    @extend_schema(responses= UserCommentsListSerialzier, tags = ['Comments'], summary = 'To get logged in user all comments')
    def get(self, request):
        comments = Comment.objects.filter(user = request.user). select_related('post')
        serializer = UserCommentsListSerialzier(comments, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
