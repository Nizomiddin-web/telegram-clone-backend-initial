from django.urls import path, include
from rest_framework.routers import DefaultRouter

from group.views import GroupApiViewSet

router = DefaultRouter()
router.register('',GroupApiViewSet,basename='group-crud')

urlpatterns = [
    path('',include(router.urls))
]