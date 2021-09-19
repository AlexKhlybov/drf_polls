  
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request
from .models import Vote


class IsVoteOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request: Request, view, vote: Vote):
        return bool(
            request.method in SAFE_METHODS
            or str(request.session['user_uuid']) == vote.user
            or request.user.is_superuser
        )
