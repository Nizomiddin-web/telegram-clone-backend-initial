from django.contrib.auth import get_user_model
from django.shortcuts import render
from django_redis import get_redis_connection
from drf_spectacular.utils import extend_schema_view
from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.response import Response

from share.utils import check_otp
from user.serializers import SignUpSerializer, SignUpResponseSerializer, VerifyOTPSerializer
from user.services import UserService

User = get_user_model()

# Create your views here.
redis_conn = get_redis_connection("default")
@extend_schema_view(

)
class SignUpView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        phone_number = serializer.validated_data.get('phone_number')
        otp_secret = redis_conn.get(f"{phone_number}:otp_secret").decode()
        data = {
            "phone_number":phone_number,
            "otp_secret":otp_secret
        }
        serializer = SignUpResponseSerializer(instance=data)
        return Response(data=serializer.data,status=status.HTTP_201_CREATED)

class VerifyView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = VerifyOTPSerializer
    http_method_names = ['patch']

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data.get('phone_number')
        otp_code = serializer.validated_data.get('otp_code')
        otp_secret = kwargs.get('otp_secret')
        check_otp(phone_number,otp_code,otp_secret)
        user = User.objects.get(phone_number=phone_number,is_verified=False)
        user.is_verified=True
        user.save()
        tokens = UserService.create_tokens(user)
        return Response(data=tokens)