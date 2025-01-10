from django.urls import path, include
from rest_framework.routers import DefaultRouter

from chat.views import ChatCrudApiView

routers = DefaultRouter()
routers.register('',ChatCrudApiView,basename='chat-crud-api')
urlpatterns = [
    path('',include(routers.urls))
]