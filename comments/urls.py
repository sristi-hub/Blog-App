from django.urls import path
from . import views

urlpatterns = [
    path('create-comment/<int:post_id>/', views.CommentCreateView.as_view()),
    path('list-comments/<int:post_id>/', views.CommentsListView.as_view()),
    path('user-comments/', views.UserCommentsListView.as_view())
]