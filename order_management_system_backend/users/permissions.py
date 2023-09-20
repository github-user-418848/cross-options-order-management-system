from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow the owner of an object to edit it.
    """
    # def has_object_permission(self, request, view, obj):
    #     # Read permissions are allowed to any request, so we'll always allow GET, HEAD, or OPTIONS requests.
    #     if request.method in permissions.SAFE_METHODS:
    #         return True

    #     # Write permissions are only allowed to the owner of the object.
    #     return obj.id == request.user.id
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request, so we'll always allow GET, HEAD, or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object.
        if request.user.is_authenticated and obj.id == request.user.id:
            return True

        return False