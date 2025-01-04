import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.user.manager import UserManager


# Create your models here.
class User(AbstractUser):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    phone_number = models.CharField(max_length=18,unique=True)
    bio = models.CharField(max_length=200,null=True,blank=True)
    user_name =  models.CharField(max_length=200,null=True,blank=True,unique=True)
    birth_date = models.DateField(null=True,blank=True)
    is_verified = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(null=True,blank=True)
    is_2fa_enabled = models.BooleanField(default=False)
    otp_secret = models.CharField(max_length=200,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    username = models.CharField(max_length=200,null=True,blank=True)
    USERNAME_FIELD = "phone_number"
    objects = UserManager()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']

class UserAvatar(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    avatar = models.ImageField(upload_to="avatars/",verbose_name="Profile Photos")
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="avatars")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_avatar'
        verbose_name = "User Avatar"
        verbose_name_plural = "Users Avatar"
        ordering = ['-created_at']

class DeviceInfo(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='devices')
    device_name = models.CharField(max_length=200)
    ip_address = models.CharField(max_length=20)
    last_login = models.DateTimeField(null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'device_info'
        verbose_name = 'Device Info'
        verbose_name_plural = 'Devices Info'
        ordering = ['-created_at']

    def __str__(self):
        return f"User:{self.user} Device:{self.device_name}"

class Contact(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='contacts')
    friend = models.OneToOneField(User,on_delete=models.SET_NULL,null=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40,null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'contact'
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'
        ordering = ['-created_at']