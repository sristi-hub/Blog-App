from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from .managers import CustomUserManager
from django.core.validators import RegexValidator
from django.utils import timezone
from datetime import timedelta


contact_validator = RegexValidator(
    regex=r'^9\d{9}$',
    message="Enter a valid 10-digit Nepal mobile number starting with 9."
)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=255)
    full_name = models.CharField(max_length=255, blank=True)
    contact = models.CharField(
        max_length=10,
        blank=True,
        validators=[contact_validator]
    )

    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

class VerifyToken(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, null = True, related_name = 'verify_tokens')
    token = models.CharField(max_length = 6, null = True)
    created_at = models.DateTimeField(default = timezone.now())
    expired_at = models.DateTimeField(default = (timezone.now() + timedelta(minutes = 15)))
    
    def is_expired(self):
        return timezone.now() > self.expired_at

    def __str__(self):
        return f"{self.user.email} - {self.token}"

