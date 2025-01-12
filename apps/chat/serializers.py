from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from chat.models import Chat, Message
from user.serializers import UserProfileSerializer
User = get_user_model()

class ChatSerializer(serializers.ModelSerializer):
    owner_id = serializers.CharField(write_only=True)
    user_id = serializers.CharField(write_only=True)
    owner = UserProfileSerializer(read_only=True)
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = Chat
        fields = ['id', 'owner', 'user', 'created_at', 'owner_id', 'user_id']
        extra_kwargs = {"created_at": {"read_only": True}}

    def create(self, validated_data):
        owner_id = validated_data.get('owner_id')
        user_id = validated_data.get('user_id')
        owner = User.objects.get(id=owner_id)
        user = User.objects.get(id=user_id)
        if owner == user:
            raise ValidationError("owner and user is equals")
        if Chat.objects.filter(owner=owner, user=user).exists():
            raise ValidationError("this chat already exists!")
        return Chat.objects.create(owner=owner, user=user)


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'