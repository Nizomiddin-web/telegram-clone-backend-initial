from django.urls import path

from user.views import SignUpView, VerifyView, LoginView, UserProfileView

urlpatterns = [
    path('register/',SignUpView.as_view(),name='user-register'),
    path('verify/<str:otp_secret>/',VerifyView.as_view(),name='user-verify'),
    path('login/',LoginView.as_view(),name='user-login'),
    path('profile/',UserProfileView.as_view(),name='user-login'),
]