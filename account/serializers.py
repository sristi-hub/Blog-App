from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import User, EmailVerificationToken, ForgotPasswordToken
from django.utils import timezone
from datetime import timedelta

class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'password',
            'full_name',
            'contact'
        ]

    def validate_contact(self, value):
            if value:
                if not value.isdigit():
                    raise serializers.ValidationError("Contact must contain only digits.")
                if len(value) != 10:
                    raise serializers.ValidationError("Contact number must be exactly 10 digits.")
                if not value.startswith('9'):
                    raise serializers.ValidationError("Nepal mobile numbers must start with 9.")
            return value
    def create(self, validated_data):
        user = User.objects.create_user(
        email = validated_data['email'],
        password = validated_data['password'],
        contact = validated_data['contact'],
        full_name = validated_data['full_name'])
        return user

class UserGetSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
                'email',
                'full_name',
                'contact',
                'is_verified',
                'last_login',
                'created_at',
                'user_permissions',
                'is_active'
            ]

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError('Invalid credentials.')
        attrs['user'] = user
        return attrs
    
class GenerateTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.CharField(max_length = 6)
    new_password = serializers.CharField(write_only = True)
    confirm_password = serializers.CharField(write_only = True)

    def validate(self, attrs):
        # Validate user
        try:
            user = User.objects.get(email=attrs['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")

        # Validate token
        try:
            verify_obj = ForgotPasswordToken.objects.get(user=user, token=attrs['token'])
        except ForgotPasswordToken.DoesNotExist:
            raise serializers.ValidationError("Invalid token.")
        
        # Check expiration
        if verify_obj.expired_at < timezone.now():
            raise serializers.ValidationError("Token has expired.")
        
        if attrs['confirm_password'] != attrs['new_password']:
            raise serializers.ValidationError('New password and Confirm password does not match. ')

        attrs['user'] = user
        attrs['verify_obj'] = verify_obj
        attrs['new_password'] = attrs['new_password']
        return attrs


class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.CharField(max_length=6)

    def validate(self, attrs):
        # Validate user
        try:
            user = User.objects.get(email=attrs['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")

        # Validate token
        try:
            verify_obj = EmailVerificationToken.objects.get(user=user, token=attrs['token'])
        except EmailVerificationToken.DoesNotExist:
            raise serializers.ValidationError("Invalid token.")

        # Check expiration
        if verify_obj.expired_at < timezone.now():
            raise serializers.ValidationError("Token has expired.")

        attrs['user'] = user
        attrs['verify_obj'] = verify_obj
        return attrs



    
