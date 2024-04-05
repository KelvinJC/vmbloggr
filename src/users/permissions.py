from rest_framework import permissions

class IsUserOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Check if the user is the owner of the account
        return obj.email == request.user.email
