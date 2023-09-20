from rest_framework import permissions

class IsAdminOrSuperadminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow admin and superadmin users to perform update and delete actions.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user and (request.user.is_staff or request.user.is_superuser)

class IsSuperadminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow superusers to delete trades.
    """
    
    def has_permission(self, request, view):
            if request.method in permissions.SAFE_METHODS:
                return True

            return request.user and (request.user.is_superuser and request.user.is_staff)