from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, VerifyToken
from account.serializers import UserCreateSerializer, UserGetSerializer, LoginSerializer, VerifyEmailSerializer, GenerateTokenSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
import random
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

#Generate JWT token
def generate_tokens(user, message='Success'):
    refresh = RefreshToken.for_user(user)
    access = refresh.access_token
    return Response({
        'message': message,
        'data': {
            'access': str(access),
            'refresh': str(refresh)
        }
    }, status=status.HTTP_201_CREATED)


#Generate email verification token
def generate_6digit_token():
    '''Generate 6 digit token as a string'''
    return f"{random.randint(0, 999999):06d}"

def create_or_update_verification_token(user, token):
    VerifyToken.objects.update_or_create(
        user = user,
        defaults = {
            "created_at" : timezone.now(),
            "expired_at" : timezone.now() + timedelta(minutes = 15),
            "token" : token
        }
    )
    

def send_verification_email(user, token):
    frontend_url = "https://sriti.com/verify-email"
    verification_link = f"{frontend_url}?token={token}&email={user.email}"
    send_mail(
        subject = "Verify your account",
        message = f"Click this link to verify your email: {verification_link}",
        from_email = settings.DEFAULT_FROM_EMAIL,
        recipient_list = [user.email],
        fail_silently = False  

    )
    return verification_link


class RegisterView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserCreateSerializer

    @extend_schema(
        request=UserCreateSerializer, tags=['Authentication'], summary='Create a new user.')
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # return generate_tokens(user, 'Register success.')

        token = generate_6digit_token()
        create_or_update_verification_token(user, token)
        send_verification_email(user, token)

        return Response({'message':'Registered Successfully, Verfication email has been sent to your email'}, status = status.HTTP_201_CREATED)

class UserView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserGetSerializer
    

    @extend_schema(tags=['Authentication'], summary='Get currently logged in user details.')
    def get(self, request):
        user = request.user
        serializer = UserGetSerializer(user)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)


class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    @extend_schema(request=LoginSerializer, tags=['Authentication'], summary='Login with existing credentials.')
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        return generate_tokens(user, 'Login success.')
    
class GenerateTokenView(APIView):
    permission_classes = [IsAuthenticated] 
    serializer_class = GenerateTokenSerializer

    @extend_schema(request=GenerateTokenSerializer, tags = ['Authentication'], summary = 'Generate token for email verification')
    def post(self, request):
        serializer = GenerateTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = User.objects.get(email=email)
        if not user:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Generate and save token
        token = generate_6digit_token()
        create_or_update_verification_token(user, token)
        verification_link = send_verification_email(user, token)


        return Response({
            'message': 'Verification token generated and sent!',
            'verification_link': verification_link
        })
    

class VerifyEmail(APIView):
    permission_classes = [AllowAny]
    serializer_class = VerifyEmailSerializer
    @extend_schema(request=VerifyEmailSerializer, tags = ['Authentication'], summary = 'Verify email using token')
    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        verify_obj = serializer.validated_data['verify_obj']


        user.is_verified = True  
        user.save()

        # Delete token after verification
        verify_obj.delete()

        return Response({'message': 'Email verified successfully.'}, status=status.HTTP_200_OK)
    
