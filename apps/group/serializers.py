from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from chat.serializers import UserSerializer
from group.models import Group, GroupPermission
User = get_user_model()

class GroupSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    class Meta:
        model = Group
        fields = ['id','name','is_private','owner','created_at']

class GroupPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupPermission
        fields = ['can_send_messages','can_send_media']

class GroupMemberSerializer(serializers.ModelSerializer):
    members = PrimaryKeyRelatedField(queryset=User.objects.all(),many=True)
    class Meta:
        model = Group
        fields = ['members']