
from core.base.permissions import (
    BasePermissionSet,
)

from rest_framework.permissions import AllowAny


class AttendPermissionSet(BasePermissionSet):

    list_perms = [AllowAny, ]
    create_perms = [AllowAny, ]


class SuscriptorPermissionSet(BasePermissionSet):

    list_perms = [AllowAny, ]
    create_perms = [AllowAny, ]


class ContactPermissionSet(BasePermissionSet):

    list_perms = [AllowAny, ]
    create_perms = [AllowAny, ]