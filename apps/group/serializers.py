from rest_framework import serializers

from chat.serializers import UserSerializer
from group.models import Group, GroupPermission


class GroupSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    class Meta:
        model = Group
        fields = ['id','name','is_private','owner','created_at']

class GroupPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupPermission
        fields = ['can_send_messages','can_send_media']