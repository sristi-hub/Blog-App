from django.urls import path

from account.views import RegisterView, LoginView, UserView, GenerateTokenView, VerifyEmail

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('user/', UserView.as_view()),
    path('generate-token/', GenerateTokenView.as_view()),
    path('verify-email', VerifyEmail.as_view())

]