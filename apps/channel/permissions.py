from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsChannelOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.owner==request.user

class IsChannelPrivate(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if obj.channel_type=='private':
            return obj.owner==request.user
        return True

class IsChannelOwnerAndLeftMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.method=='DELETE':
            return True
        return obj.owner == request.user

class ChannelMessageOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.channel.owner == request.user

class IsChannelMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user in obj.channel.memberships.all()