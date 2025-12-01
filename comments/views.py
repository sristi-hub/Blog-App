from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import AllowAny
from account.permissions import IsAdmin, IsUser, IsModerator, IsModeratorOrAdmin, IsUserOrModerator
from rest_framework import status
from posts.models import Post
from .models import Comment
from .serializers import CommentCreateSerializer, CommentsListSerializer, UserCommentsListSerialzier, CommentStatusUpdateSerializer
from drf_spectacular.utils import extend_schema
# Create your views here.


class CommentCreateView(APIView):
    permission_classes = [IsUser]
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
    permission_classes = [IsUserOrModerator]
    serializer_class = CommentsListSerializer

    @extend_schema(responses = CommentsListSerializer, tags = ['Comments'], summary = 'List comments (with replies) of a post')
    def get(self, request, post_id):
        comments = Comment.objects.filter(post_id = post_id, parent = None, status = 'approved')
        serializer = CommentsListSerializer(comments, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
class UserCommentsListView(APIView):
    permission_classes = [IsUser]
    serializer_class = UserCommentsListSerialzier

    @extend_schema(responses= UserCommentsListSerialzier, tags = ['Comments'], summary = 'To get logged in user all comments')
    def get(self, request):
        allcomments = Comment.objects.filter(user = request.user, status = 'approved'). select_related('post')
        comments = allcomments.filter(parent__isnull = True)
        replies = allcomments.filter(parent__isnull = False)
        return Response({
            "comments": UserCommentsListSerialzier(comments, many = True).data,
            "replies": UserCommentsListSerialzier(replies, many = True).data,
        }, status = status.HTTP_200_OK)
    
class CommentPendingView(APIView):
    permission_classes = [IsModeratorOrAdmin]

    @extend_schema(tags = ['Moderator'], summary = "To update comment status")
    def get(self, request):
        comment = Comment.objects.filter(status = 'pending')
        serializer = CommentsListSerializer(comment, many = True)
        count = comment.count()
        return Response({'count': count,'data' :serializer.data}, status = status.HTTP_200_OK)
    
class CommentStatusUpdateView(APIView):
    permission_classes = [IsModeratorOrAdmin]
    serializer_class = CommentStatusUpdateSerializer

    @extend_schema(tags = ['Moderator'], summary = "To update comment status")
    def patch(self, request, pk):
        try:
            comment = Comment.objects.get(id = pk)
        except Comment.DoesNotExist:
            return Response(
                {'message': "Comment does not exist"},
                 status = status.HTTP_404_NOT_FOUND
            )
        
        if 'status' not in request.data:
            return Response(
                {'status': ['This field is required']},
                status = status.HTTP_400_BAD_REQUEST
            )
        serializer = CommentStatusUpdateSerializer(comment, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
