from rest_framework import permissions

class IsBlogPostAuthorOrReadOnly(permissions.BasePermission):
    ''' Restrict update, partial update and delete requests to blog post author.'''
    
    def has_object_permission(self, request, view, obj):
        # allow GET, HEAD, and OPTIONS requests (read-only)
        if request.method in permissions.SAFE_METHODS:
            return True
        # check if the requesting user is the owner of the blog post
        return obj.author == request.user