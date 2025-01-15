from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


from chat.models import Chat, Message, ChatParticipant
from user.serializers import UserProfileSerializer
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "phone_number", "user_name", "bio", "birth_date", "first_name", "last_name"]

class ChatParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatParticipant
        fields = '__all__'

class ChatSerializer(serializers.ModelSerializer):
    owner_id = serializers.UUIDField(write_only=True)
    user_id = serializers.UUIDField(write_only=True)
    owner = UserProfileSerializer(read_only=True)
    user = UserProfileSerializer(read_only=True)
    participants = serializers.JSONField(default=list,read_only=True)

    class Meta:
        model = Chat
        fields = ['id', 'owner', 'user', 'created_at', 'owner_id', 'user_id','participants']
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
    sender = serializers.StringRelatedField()  # Or another appropriate serialization
    liked_by = UserSerializer(many=True,read_only=True)  # Liked users
    chat = ChatSerializer(required=False)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'chat', 'sender', 'text', 'image', 'file', 'sent_at', 'is_read', 'liked_by', 'likes_count']

    def get_likes_count(self, obj):
        return obj.liked_by.count()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['id'] = str(representation['id'])
        return representation

    def create(self, validated_data):
        liked_by_data = validated_data.pop('liked_by', None)

        message = Message.objects.create(**validated_data)

        if liked_by_data:
            for user in liked_by_data:
                message.liked_by.add(user)

        return message

