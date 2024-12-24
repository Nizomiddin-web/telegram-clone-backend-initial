from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.user.manager import UserManager


# Create your models here.
class User(AbstractUser):
    phone_number = models.CharField(max_length=16,unique=True)
    bio = models.CharField(max_length=200,null=True,blank=True)
    user_name =  models.CharField(max_length=200,null=True,blank=True)
    birth_date = models.DateField(null=True,blank=True)
    is_verified = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(null=True,blank=True)
    is_2fa_enabled = models.BooleanField(default=False)
    otp_secret = models.CharField(max_length=16,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    USERNAME_FIELD = "phone_number"
    objects = UserManager()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']