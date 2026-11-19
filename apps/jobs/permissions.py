
from rest_framework.permissions import BasePermission


class IsEmployer(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'EMPLOYER'
        )


class IsEmployerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in ['EMPLOYER', 'ADMIN']
        )

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'ADMIN':
            return True

        return (
            request.user.role == 'EMPLOYER'
            and obj.employer.user_id == request.user.id
        )
