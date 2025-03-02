from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user.views import SignUpView, VerifyView, LoginView, UserProfileView, UserAvatarUploadView, \
    UserAvatarRetrieveDeleteView, DeviceListView, LogoutView, ContactApiView, ContactSycnApiView, Enable2FAView, \
    Verify2FAView, UserPresenceApiView, NotificationPreferenceApiView

router = DefaultRouter()
router.register(r'',ContactApiView,basename='contact')

urlpatterns = [
    path('register/',SignUpView.as_view(),name='user-register'),
    path('verify/<str:otp_secret>/',VerifyView.as_view(),name='user-verify'),
    path('login/',LoginView.as_view(),name='user-login'),
    path('profile/',UserProfileView.as_view(),name='user-profile'),
    path('avatars/',UserAvatarUploadView.as_view(),name='user-avatar-list-create'),
    path('avatars/<uuid:pk>/',UserAvatarRetrieveDeleteView.as_view(),name='user-avatar-retrieve-delete'),
    path('devices/',DeviceListView.as_view(),name='user-devices'),
    path('logout/',LogoutView.as_view(),name='user-logout'),
    path('2fa/',Enable2FAView.as_view(),name='user-2fa'),
    path('2fa/verify/',Verify2FAView.as_view(),name='user-2fa-verify'),
    path('<uuid:pk>/status/',UserPresenceApiView.as_view(),name='user-status'),
    path('notifications/',NotificationPreferenceApiView.as_view(),name='user-notification'),
    path('contacts/sync/',ContactSycnApiView.as_view(),name='contact-sync'),
    path('contacts/',include(router.urls)),

]