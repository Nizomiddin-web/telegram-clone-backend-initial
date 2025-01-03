import re

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework.generics import get_object_or_404

from share.tasks import send_email_task, send_sms_task
from share.utils import generate_otp, check_otp
from user.models import UserAvatar, DeviceInfo

User = get_user_model()

class SignUpSerializer(serializers.Serializer):
    phone_number = serializers.CharField(min_length=9,max_length=16,help_text="bu telefon raqam")

    def validate_phone_number(self,phone_number):
        pattern = r"^\+?[1-9]\d{1,16}$"
        if re.match(pattern,phone_number):
            if User.objects.filter(phone_number=phone_number,is_verified=True).exists():
                raise ValidationError(_("User with this phone number already exists"))
            return phone_number
        raise ValidationError(_("Phone number not is valid"))

    def create(self, validated_data):
        phone_number = validated_data.get('phone_number')
        user = User.objects.get_or_create(**validated_data)
        otp_code,otp_secret = generate_otp(phone_number=phone_number,expire_in=2*60)
        send_email_task.delay(email="nizomiddinmaniyev99@gmail.com",otp_code=otp_code)
        # send_sms_task.delay(phone_number=phone_number,otp_code=otp_code)
        return user

class SignUpResponseSerializer(serializers.Serializer):
    phone_number = serializers.CharField(min_length=9,max_length=16,help_text="Bu telefon raqam uchun",read_only=True)
    otp_secret = serializers.CharField(max_length=20,read_only=True)

class VerifyOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(min_length=9,max_length=18)
    otp_code = serializers.CharField(max_length=6)

    def validate_phone_number(self,phone_number):
        pattern = r"^\+?[1-9]\d{1,16}$"
        if re.match(pattern,phone_number):
            return phone_number
        raise ValidationError(_("Phone number not is valid"))

    def create(self, validated_data):
        phone_number = validated_data.get('phone_number')
        otp_code = validated_data.get('otp_code')
        otp_secret = self.context.get('otp_secret')
        check_otp(phone_number, otp_code, otp_secret)
        user = get_object_or_404(User, phone_number=phone_number)
        user.is_verified = True
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(min_length=9, max_length=18)

    def validate_phone_number(self, phone_number):
        pattern = r"^\+?[1-9]\d{1,16}$"
        if re.match(pattern, phone_number):
            return phone_number
        raise ValidationError(_("Phone number not is valid"))

    def create(self, validated_data):
        phone_number = validated_data.get('phone_number')
        user = get_object_or_404(User, phone_number=phone_number)
        otp_code,otp_secret = generate_otp(phone_number,expire_in=5*60)
        send_email_task.delay(email="nizomiddinmaniyev99@gmail.com",otp_code=otp_code)
        # send_sms_task.delay(phone_number,otp_code)
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(max_length=200,allow_null=True,allow_blank=True)
    def validate_user_name(self,user_name):
        if user_name=="":
            raise ValidationError("User name cannot be empty.")
        return user_name

    class Meta:
        model = User
        fields = ['id','phone_number','user_name','bio','birth_date','first_name','last_name']
        extra_kwargs = {'id':{'read_only':True},'phone_number':{'read_only':True}}

class UserAvatarSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField()
    class Meta:
        model = UserAvatar
        fields = ['id','avatar']
        extra_kwargs = {'id':{'read_only':True}}

class DeviceInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceInfo
        fields = ['device_name','ip_address','last_login']