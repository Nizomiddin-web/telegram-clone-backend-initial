from django.urls import path, include
from rest_framework.routers import DefaultRouter

from channel.views import ChannelApiView, ChannelMembershipListCreateApiView, ChannelMembershipUpdateDestroyApiView

router = DefaultRouter()
router.register('',ChannelApiView,basename='channel-crud')

urlpatterns = [
    path('<uuid:pk>/memberships/',ChannelMembershipListCreateApiView.as_view(),name='create-list-members'),
    path('<uuid:id>/memberships/<uuid:member_id>/',ChannelMembershipUpdateDestroyApiView.as_view(),name='create-list-members'),
    path('',include(router.urls))
]