from rest_framework.permissions import BasePermission


class AdminUsernameAPIPermission(BasePermission):
    def has_permission(self, request, view):
        return (
            True if request.user.username in ['adminAPI', 'admin']
            else False
        )
