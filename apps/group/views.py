from django.db.models import Q
from django.shortcuts import render
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from sentry_sdk.integrations.beam import raise_exception

from group.models import Group, GroupPermission
from group.permissions import IsGroupOwnerOrReadOnly, IsGroupOwnerUsePermission
from group.serializers import GroupSerializer, GroupPermissionSerializer
from user.paginations import CustomPagination


# Create your views here.


class GroupApiViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated,IsGroupOwnerOrReadOnly]
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.action=='list':
            return self.queryset.filter(Q(members=self.request.user) | Q(owner=self.request.user))
        return super().get_queryset()

    def perform_create(self, serializer):
        group = serializer.save(owner=self.request.user)
        GroupPermission.objects.create(group=group)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.owner!=request.user:
            raise NotFound(detail="Bu sizga tegishli guruh emas!")
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class GroupPermissionsApi(UpdateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupPermissionSerializer
    permission_classes = [IsGroupOwnerOrReadOnly,]
    http_method_names = ['patch']

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            instance=GroupPermission.objects.get(group=instance)
        except GroupPermission.DoesNotExist:
            return Response({"detail": "Group permission not found"},status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance,request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

