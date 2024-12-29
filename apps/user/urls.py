from django.urls import path

from user.views import SignUpView, VerifyView, LoginView, UserProfileView, UserAvatarUploadView, \
    UserAvatarRetrieveDeleteView, DeviceListView

urlpatterns = [
    path('register/',SignUpView.as_view(),name='user-register'),
    path('verify/<str:otp_secret>/',VerifyView.as_view(),name='user-verify'),
    path('login/',LoginView.as_view(),name='user-login'),
    path('profile/',UserProfileView.as_view(),name='user-profile'),
    path('avatars/',UserAvatarUploadView.as_view(),name='user-avatar-list-create'),
    path('avatars/<uuid:pk>/',UserAvatarRetrieveDeleteView.as_view(),name='user-avatar-retrieve-delete'),
    path('devices/',DeviceListView.as_view(),name='user-devices'),
]