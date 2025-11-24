from django.urls import path
from . import views

urlpatterns = [
    path('like/<int:post_id>/', views.LikePostView.as_view()),
    path('totallike/<int:post_id>/', views.PostLikeView.as_view()),
    path('mylikes/', views.UserLikeView.as_view()),
    path('bookmarks/<int:post_id>/', views.PostBookmarkCreateView.as_view()),
    path('mybookmarks/', views.UserBookmarkView.as_view()),
    path('follow/<int:author_id>', views.FollowView.as_view()),
    path('myfollowers/', views.UserFollowersView.as_view()),
    path('myfollowings/', views.UserFollowingView.as_view()),
]