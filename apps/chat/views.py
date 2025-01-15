from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import Q
from rest_framework import status
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from chat.models import Chat, Message
from chat.serializers import ChatSerializer, MessageSerializer
from user.paginations import CustomPagination


# Create your views here.

class ChatCrudApiView(ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    http_method_names = ['get','post','delete']
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        if self.action=='list':
            return self.queryset.filter(Q(owner=self.request.user) | Q(user=self.request.user))
        return super().get_queryset()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.owner !=request.user:
            return Response(data={"detail":"User is not chat owner"},status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        if instance.owner != self.request.user:
            raise NotFound("User is not chat owner")
        instance.delete()

class MessageListCreateView(ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated,]

    def perform_create(self, serializer):
        chat_id = self.kwargs.get('pk')
        chat = Chat.objects.get(pk=chat_id)
        message = serializer.save(sender=self.request.user,chat=chat)
        if message.file or message.image:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"chat_{message.chat.id}",
                {
                    "type":"chat_message",
                    "message_id":str(message.id),
                    "sender":{
                        "id":str(message.sender.id),
                        "user_name":str(message.sender.username),
                    },
                    "text":message.text,
                    "image":message.image.url if message.image.url else None,
                    "file":message.file if message.file else None,
                    "sent_at":message.sent_at.isoformat()
                },
            )

