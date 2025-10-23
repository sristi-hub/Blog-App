from django.urls import path

from account.views import RegisterView, LoginView, UserView, GenerateTokenView, VerifyEmail, ForgotPasswordView, PasswordResetView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('user/', UserView.as_view()),
    path('generate-token/', GenerateTokenView.as_view()),
    path('verify-email/', VerifyEmail.as_view()),
    path('forgot-password/', ForgotPasswordView.as_view() ),
    path('password-reset/', PasswordResetView.as_view()),

]