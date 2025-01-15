from django.urls import path, include
from rest_framework.routers import DefaultRouter

from chat.views import ChatCrudApiView, MessageListCreateView

routers = DefaultRouter()
routers.register('',ChatCrudApiView,basename='chat-crud-api')
urlpatterns = [
    path('<uuid:pk>/messages/',MessageListCreateView.as_view(),name='chat-message-list-create'),
    path('',include(routers.urls))
]