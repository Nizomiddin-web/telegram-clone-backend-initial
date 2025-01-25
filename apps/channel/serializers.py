from rest_framework import serializers

from channel.models import Channel
from chat.serializers import UserSerializer


class ChannelSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    class Meta:
        model = Channel
        fields = ['id','name','description','channel_type','created_at','owner']