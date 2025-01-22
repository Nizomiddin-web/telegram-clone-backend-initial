from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from chat.serializers import UserSerializer
from group.models import Group, GroupPermission, GroupMessage

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

class GroupMessageSerializer(serializers.ModelSerializer):
    group = GroupSerializer(read_only=True)
    sender = UserSerializer(read_only=True)
    liked_by = UserSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = GroupMessage
        fields = ['id','group','sender','text','image','file','sent_at','is_read','liked_by','likes_count']
        read_only_fields = ['liked_by']

    def get_likes_count(self,obj):
        return obj.liked_by.count()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['id'] = str(representation['id'])
        return representation