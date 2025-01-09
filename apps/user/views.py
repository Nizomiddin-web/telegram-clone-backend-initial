from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, check_password
from django_redis import get_redis_connection
from drf_spectacular.utils import extend_schema_view
from rest_framework import status
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.generics import CreateAPIView, UpdateAPIView, \
    ListCreateAPIView, DestroyAPIView, RetrieveAPIView, RetrieveUpdateAPIView, ListAPIView, get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from sentry_sdk.integrations.beam import raise_exception

from share.enums import TokenType
from share.services import TokenService
from user.models import UserAvatar, DeviceInfo, Contact
from user.paginations import CustomPagination
from user.permissions import IsUserVerify, IsContactUser
from user.serializers import SignUpSerializer, SignUpResponseSerializer, VerifyOTPSerializer, LoginSerializer, \
    UserProfileSerializer, UserAvatarSerializer, DeviceInfoSerializer, ContactSerializer, ContactSyncSerializer, \
    Request2FASerializer, Verify2FARequestSerializer
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
        serializer = self.get_serializer(data=request.data,context={"otp_secret":kwargs.get('otp_secret')})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user.is_2fa_enabled:
            data = {
             "detail": "2FA enabled, please verify your password",
             "user_id": user.id
            }
            return Response(data=data)
        tokens = UserService.create_tokens(user)
        return Response(data=tokens)

class LoginView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    permission_classes = [AllowAny,]
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data.get('phone_number')
        user = serializer.save()
        otp_secret = redis_conn.get(f"{user.phone_number}:otp_secret").decode()
        data = {
            "phone_number":phone_number,
            "otp_secret":otp_secret
        }
        return Response(data=data)

class UserProfileView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsUserVerify,]
    http_method_names = ['get','patch']

    def retrieve(self, request, *args, **kwargs):
        print(TokenService.get_valid_tokens(request.user.id,TokenType.ACCESS))
        serializer = self.get_serializer(instance=request.user)
        return Response(data=serializer.data)

    def patch(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(user,request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class UserAvatarUploadView(ListCreateAPIView):
    queryset = UserAvatar.objects.all()
    serializer_class = UserAvatarSerializer
    permission_classes = [IsUserVerify,]
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserAvatarRetrieveDeleteView(RetrieveAPIView,DestroyAPIView):
    queryset = UserAvatar.objects.all()
    serializer_class = UserAvatarSerializer
    permission_classes = [IsUserVerify]

class DeviceListView(ListAPIView):
    queryset = DeviceInfo.objects.all()
    serializer_class = DeviceInfoSerializer
    permission_classes = [IsUserVerify]
    pagination_class = CustomPagination

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated,]
    def post(self,request,*args,**kwargs):
        user = request.user
        TokenService.delete_tokens(user.id,TokenType.ACCESS)
        TokenService.delete_tokens(user.id,TokenType.REFRESH)
        TokenService.add_token_to_redis(user.id,"fake_token",TokenType.ACCESS,settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'])
        TokenService.add_token_to_redis(user.id,"fake_token",TokenType.REFRESH,settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'])
        # UserService.create_tokens(user=request.user,access="fake_token",refresh="fake_token")
        return Response(data={"detail":"Successfully logged out"})

class ContactApiView(ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.action=='list':
            return self.queryset.filter(user=self.request.user)
        return super().get_queryset()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        if self.request.user==instance.user:
            instance.delete()
        else:
            raise NotFound(detail="error")

class ContactSycnApiView(CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSyncSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data,many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response(serializer.data,status=status.HTTP_201_CREATED)

class Enable2FAView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = Request2FASerializer
    permission_classes = [IsAuthenticated,]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(["OTP secret must be at least 8 characters long."],status=status.HTTP_400_BAD_REQUEST)
        type = serializer.validated_data.get('type')
        otp_secret = serializer.validated_data.get('otp_secret',None)
        user = request.user
        if type:
            user.is_2fa_enabled=True
            user.otp_secret = make_password(otp_secret)
            user.save()
            return Response({"detail":"2FA enabled."},)
        else:
            user.is_2fa_enabled=False
            user.otp_secret=None
            user.save()
            return Response({"detail":"2FA disabled."})

class Verify2FAView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = Verify2FARequestSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = serializer.validated_data.get('user_id')
        password = serializer.validated_data.get('password')
        user = User.objects.filter(id=user_id).first()
        if not user:
            return Response({"detail":"Invalid user"},status=status.HTTP_400_BAD_REQUEST)
        if check_password(password,user.otp_secret):
            tokens = UserService.create_tokens(user)
            return Response(tokens)
        return Response({"detail":"Invalid password"},status=status.HTTP_400_BAD_REQUEST)

