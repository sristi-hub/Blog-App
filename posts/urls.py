from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('category/', views.CategoryViews.as_view()),
    path('postslist/', views.PostListAPIView.as_view()),
    path('postslist/<int:pk>', views.RetrievePost.as_view()),
    path('mine-postslist/', views.UserPostListAPIView.as_view()),
    # path('filter-postslist/', views.FilterPostByUser.as_view()),
    # path('postslist/author/<str:author>', views.FilterPostByUser.as_view()),
    path('post-create/', views.PostCreateAPIView.as_view()),
    path('post-delete/<int:pk>', views.PostDeleteAPIView.as_view()),
    path('post-update/<int:pk>/', views.PostEditAPIView.as_view()),
    path('postfilter/', views.FilterView.as_view()),
]

# router = DefaultRouter()
# router.register('postslist', views.PostListViewset)
# urlpatterns += router.urls