from django.db.models import Q
from django.shortcuts import render
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import UpdateAPIView, RetrieveDestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from sentry_sdk.integrations.beam import raise_exception

from group.models import Group, GroupPermission, GroupParticipant
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

class GroupMembershipApiView(RetrieveDestroyAPIView,CreateAPIView):
    queryset = Group.objects.all()
    permission_classes = [IsAuthenticated,]

    # def get_serializer_class(self):
    #     if self.request.GET

    def create(self, request, *args, **kwargs):
        group = self.get_object()
        if group.is_private:
            return Response({"detail":"This group is private."},status=status.HTTP_403_FORBIDDEN)
        if group.members.filter(id=request.user.id).exists():
            return Response({"detail":"You are already a member of this group."},status=status.HTTP_400_BAD_REQUEST)
        group.members.add(request.user)
        return Response({"detail":"You have successfully joined the group."},status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        group = self.get_object()
        if not group.members.filter(id=request.user.id).exists():
            return Response({"detail":"You are not a member of this group."},status=status.HTTP_400_BAD_REQUEST)
        group.members.remove(request.user)
        return Response({"detail":"You have successfully left the group."})