from django.shortcuts import render
from .models import Post, Category
from .serializers import PostListSerializer, PostCreateSerializer, CategorySerializer, EmptySerializer
from rest_framework import viewsets 
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PostFilter


# Create your views here.
class CategoryViews(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer

    @extend_schema(request = CategorySerializer, tags = ['Posts'], summary = 'Get post categories')
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many = True)
        return Response(serializer.data)
    
@extend_schema(responses = PostListSerializer, tags = ['Posts'], summary= 'View all published posts')
class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    permission_classes = [AllowAny]
    serializer_class = PostListSerializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = PostListSerializer(queryset, many = True)
        return Response({
            'count': queryset.count(),
            'results':serializer.data
            })
        
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(status = 'published')


@extend_schema(request = PostListSerializer, tags = ['Posts'], summary= 'View particular post by Id')
class RetrievePost(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    permission_classes = [AllowAny]
    serializer_class = PostListSerializer

# @extend_schema(request = PostListSerializer, tags = ['Posts'], summary = 'View particular Author post')
# class FilterPostByUser(generics.ListAPIView):
#     queryset = Post.objects.all()
#     permission_classes = [AllowAny]
#     serializer_class = PostListSerializer
#     lookup_field = 'author'
   
@extend_schema(responses = PostListSerializer, tags = ['Posts'], summary = 'View user published posts')
class User_Pub_PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = PostListSerializer

    def get_queryset(self):
        user = self.request.user 
        qr = super().get_queryset()
        return qr.filter(author = user, status = 'published')

@extend_schema(responses = PostListSerializer, tags = ['Posts'], summary = 'View user draft posts')
class User_Draft_PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = PostListSerializer

    def get_queryset(self):
        user = self.request.user
        qr = super().get_queryset()
        return qr.filter(author = user, status = 'draft')

# @extend_schema(
#     parameters=[
#         OpenApiParameter(
#             name='author',
#             description='Full name of the author to filter posts',
#             required=True,
#             type=str
#         )
#     ]
# )
# class FilterPostByUser(APIView):
#     permission_classes = [AllowAny]
#     serializer_class = PostListSerializer
#     def get(self, request):
#         full_name = request.GET.get('author', None)
#         if not full_name:
#             return Response({'message': 'Author name is required'}, status=status.HTTP_400_BAD_REQUEST)
#         posts = Post.objects.filter(author__full_name = full_name)
#         if not posts.exists():
#             return Response({'message':'Posts not found'}, status = status.HTTP_404_NOT_FOUND)
    
#         posts_serializer = PostListSerializer(posts, many = True)
#         return Response(posts_serializer.data, status = status.HTTP_200_OK)

@extend_schema(request = PostCreateSerializer, tags = ['Posts'], summary= 'Create a new post')   
class PostCreateAPIView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(author = self.request.user)
        
@extend_schema(
    request=None, 
    responses={204: None}, 
    tags=['Posts'],
    summary='Delete post by id',
)
class PostDeleteAPIView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = EmptySerializer

    def get_queryset(self):
        user = self.request.user        
        qs = super().get_queryset()
        return qs.filter(author = user)
    
@extend_schema(request = PostCreateSerializer, responses = PostListSerializer, tags = ['Posts'], summary = 'Edit post')   
class PostEditAPIView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = PostCreateSerializer

    def get_queryset(self):
            user = self.request.user        
            qs = super().get_queryset()
            return qs.filter(author = user)


@extend_schema(request = PostListSerializer, tags = ['Posts'], summary= 'Filter post')
class FilterView(generics.ListAPIView):
    queryset = Post.objects.filter(status = 'published')
    permission_classes = [AllowAny]
    serializer_class = PostListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PostFilter





    




  
