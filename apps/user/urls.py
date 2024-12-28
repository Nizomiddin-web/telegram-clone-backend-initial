from django.urls import path

from user.views import SignUpView, VerifyView

urlpatterns = [
    path('register/',SignUpView.as_view(),name='user-register'),
    path('verify/<str:otp_secret>/',VerifyView.as_view(),name='user-verify'),
]