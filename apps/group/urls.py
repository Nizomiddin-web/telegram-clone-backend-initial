from django.urls import path, include
from rest_framework.routers import DefaultRouter

from group.views import GroupApiViewSet, GroupPermissionsApi, GroupMembershipApiView, GroupMemberApiView

router = DefaultRouter()
router.register('',GroupApiViewSet,basename='group-crud')

urlpatterns = [
    path('<uuid:pk>/permissions/',GroupPermissionsApi.as_view(),name='group-permission-update'),
    path('<uuid:pk>/memberships/',GroupMembershipApiView.as_view(),name='group-membership'),
    path('<uuid:pk>/members/',GroupMemberApiView.as_view(),name='group-membership'),
    path('',include(router.urls))
]