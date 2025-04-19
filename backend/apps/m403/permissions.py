from rest_framework.permissions import BasePermission
from .models import UserUserRole


def _has_role(request, required_role):
    if not request.user.is_authenticated:
        return False
    user_roles = UserUserRole.objects.filter(user=request.user).values_list('user_role__name', flat=True)
    return required_role in user_roles


class IsEKJLUser(BasePermission):
    """Allow only users with the 'EKJL' role"""

    def has_permission(self, request, view):
        return _has_role(request, "EKJL")


class IsAdminUser(BasePermission):
    """Allow only users with the 'Admin' role"""

    def has_permission(self, request, view):
        return _has_role(request, "Admin")


class IsCoachUser(BasePermission):
    """Allow only users with the 'Coach' role"""

    def has_permission(self, request, view):
        return _has_role(request, "Coach")


class IsRefereeUser(BasePermission):
    """Allow only users with the 'Referee' role"""

    def has_permission(self, request, view):
        return _has_role(request, "Referee")


