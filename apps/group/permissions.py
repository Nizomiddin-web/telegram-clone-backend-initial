from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsGroupOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return bool(obj.owner==request.user)

class IsGroupOwnerUsePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(obj.group.owner==request.user)

class IsGroupCanSendMediaPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return bool(obj.grouppermission_set.first().can_send_media)
