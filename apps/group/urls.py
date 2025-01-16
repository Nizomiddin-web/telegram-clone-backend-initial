from django.urls import path, include
from rest_framework.routers import DefaultRouter

from group.views import GroupApiViewSet, GroupPermissionsApi

router = DefaultRouter()
router.register('',GroupApiViewSet,basename='group-crud')

urlpatterns = [
    path('<uuid:pk>/permissions/',GroupPermissionsApi.as_view(),name='group-permission-update'),
    path('',include(router.urls))
]