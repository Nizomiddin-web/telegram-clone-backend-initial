from rest_framework.permissions import BasePermission


class IsUserVerify(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_verified)

class IsContactUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user==obj.user)