from django.urls import path, include
from rest_framework.routers import DefaultRouter

from channel.views import ChannelApiView

router = DefaultRouter()
router.register('',ChannelApiView,basename='channel-crud')

urlpatterns = [
    path('',include(router.urls))
]