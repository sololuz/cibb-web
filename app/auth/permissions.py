from core.base.permissions import BasePermissionSet
from rest_framework.permissions import AllowAny


class AuthPermissionSet(BasePermissionSet):
    register_perms = [AllowAny, ]
    confirm_register_perms = [AllowAny, ]
    login_perms = [AllowAny, ]
    check_email_perms = [AllowAny, ]
    check_username_perms = [AllowAny, ]

    get_csrf_token_perms = [AllowAny, ]
