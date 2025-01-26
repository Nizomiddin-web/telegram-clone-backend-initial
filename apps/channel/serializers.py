from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from channel.models import Channel, ChannelMembership
from chat.serializers import UserSerializer
User = get_user_model()

class ChannelSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    class Meta:
        model = Channel
        fields = ['id','name','description','channel_type','created_at','owner']


class ChannelMembershipSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = ChannelMembership
        fields = ['id','user','user_id','role','joined_at']

    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        user = User.objects.filter(pk=user_id).first()
        if not user:
            raise ValidationError("user not found")
        validated_data['user'] = user
        return super().create(validated_data)
