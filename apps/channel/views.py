from django.db.models import Q
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.generics import ListCreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from channel.models import Channel, ChannelMembership, ChannelMessage
from channel.permissions import IsChannelOwner, IsChannelPrivate, IsChannelOwnerAndLeftMember, ChannelMessageOwner
from channel.serializers import ChannelSerializer, ChannelMembershipSerializer, ChannelMessageSerializer
from share.tasks import send_push_notification
from user.paginations import CustomPagination


# Create your views here.


class ChannelApiView(ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    permission_classes = [IsAuthenticated,IsChannelOwner]
    pagination_class = CustomPagination
    http_method_names = ['get','post','patch','delete']

    def get_queryset(self):
        if self.action=='list':
            return self.queryset.filter(Q(owner=self.request.user) | Q(memberships__user=self.request.user))
        return super().get_queryset()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ChannelMembershipListCreateApiView(ListCreateAPIView):
    queryset = Channel.objects.all()
    serializer_class = ChannelMembershipSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated,IsChannelPrivate]

    def list(self, request, *args, **kwargs):
        channel = self.get_object()
        memberships = ChannelMembership.objects.filter(channel=channel)
        page = self.paginate_queryset(memberships)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(page, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        channel = self.get_object()
        serializer.save(channel=channel)

class ChannelMembershipUpdateDestroyApiView(UpdateAPIView,DestroyAPIView):
    queryset = Channel.objects.all()
    serializer_class = ChannelMembershipSerializer
    http_method_names = ['patch','delete']
    lookup_field = 'id'
    permission_classes = [IsAuthenticated, IsChannelOwnerAndLeftMember]

    def get_object(self):
        if self.request.method in ['patch','delete']:
            user_id = self.kwargs.get('member_id')
            chanel_id = self.kwargs.get('id')
            member = ChannelMembership.objects.filter(Q(channel__id=chanel_id) & Q(user__id=user_id)).first()
            return member
        return super().get_object()

class ChannelMessageCreateListApiView(ListCreateAPIView):
    queryset = ChannelMessage.objects.all()
    serializer_class = ChannelMessageSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.method=='GET':
            channel_id = self.kwargs.get('channel_id')
            return self.queryset.filter(channel__id=channel_id)
        return super().get_queryset()

    def perform_create(self, serializer):
        channel_id = self.kwargs.get('channel_id')
        channel=Channel.objects.filter(pk=channel_id).first()
        if not channel:
            raise NotFound(detail="Channel Not Found")
        user = self.request.user
        if channel.owner != user:
            raise PermissionDenied(detail="Sizga ushbu kanalda xabar yaratishga ruxsat berilmagan.")
        message=serializer.save(channel=channel,sender=user)
        for membership in channel.memberships.all():
                send_push_notification.delay(str(membership.user.id),f"New Message in {channel.name}",message.text)

class ChannelMessageRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = ChannelMessage.objects.all()
    serializer_class = ChannelMessageSerializer
    permission_classes = [IsAuthenticated,ChannelMessageOwner]