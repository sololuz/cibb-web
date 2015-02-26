# -*- encoding:utf-8 -*-
from rest_framework.routers import DefaultRouter


router = DefaultRouter(trailing_slash=False)

from users.api import UsersViewSet
from auth.api import AuthViewSet

router.register('auth', AuthViewSet, base_name="auth")
router.register('users', UsersViewSet, base_name="users")
