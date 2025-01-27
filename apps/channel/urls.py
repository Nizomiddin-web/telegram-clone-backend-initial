from django.urls import path, include
from rest_framework.routers import DefaultRouter

from channel.views import ChannelApiView, ChannelMembershipListCreateApiView, ChannelMembershipUpdateDestroyApiView, \
    ChannelMessageCreateListApiView, ChannelMessageRetrieveUpdateDestroy, ChannelScheduleMessageApiView, \
    ChannelMessageLikeRemoveApiView

router = DefaultRouter()
router.register('',ChannelApiView,basename='channel-crud')


urlpatterns = [
    path('<uuid:pk>/memberships/',ChannelMembershipListCreateApiView.as_view(),name='create-list-members'),
    path('<uuid:id>/memberships/<uuid:member_id>/',ChannelMembershipUpdateDestroyApiView.as_view(),name='update-destroy-members'),
    path('<uuid:channel_id>/messages/',ChannelMessageCreateListApiView.as_view(),name='create-list-messages'),
    path('<uuid:channel_id>/messages/<uuid:pk>/',ChannelMessageRetrieveUpdateDestroy.as_view(),name='update-destroy-messages'),
    path('<uuid:channel_id>/messages/schedule/',ChannelScheduleMessageApiView.as_view(),name='create-scheduled-message'),
    path('<uuid:channel_id>/messages/<uuid:pk>/like/',ChannelMessageLikeRemoveApiView.as_view(),name='like-unlike-message'),
    path('',include(router.urls))
]