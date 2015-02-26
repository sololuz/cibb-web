
from core.base.permissions import (
    IsAuthenticated,
    BasePermissionSet,
    IsProfileOwner,
)

from rest_framework.permissions import AllowAny


class UserPermissionSet(BasePermissionSet):
    list_perms = [AllowAny, ]

    create_perms = [IsAuthenticated, IsProfileOwner, ]
    partial_update_perms = [IsAuthenticated, IsProfileOwner, ]
    get_csrf_token_perms = [IsAuthenticated, ]
    profile_perms = [IsAuthenticated, IsProfileOwner, ]
    password_change_perms = [IsAuthenticated, IsProfileOwner, ]
    password_recovery_perms = [IsAuthenticated, IsProfileOwner, ]
    password_from_recovery_perms = [AllowAny, ]
    change_email_perms = [AllowAny, ]
    cancel_perms = [AllowAny, ]

    retrieve_perms = [AllowAny, ]
    update_perms = [AllowAny, ]
    destroy_perms = [AllowAny, ]

