from django.db.models import Q
from rest_framework import status
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from chat.models import Chat
from chat.serializers import ChatSerializer
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

