from django.urls import path
from . import views

urlpatterns = [
    path('like/<int:post_id>/', views.LikePostView.as_view()),
    path('totallike/<int:post_id>/', views.PostLikeView.as_view()),
    path('mylikes/', views.UserLikeView.as_view())
]