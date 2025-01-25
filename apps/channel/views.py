from django.db.models import Q
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from channel.models import Channel
from channel.permissions import IsChannelOwner
from channel.serializers import ChannelSerializer
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
