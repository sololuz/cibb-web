# -*- encoding:utf-8 -*-
from registro.api import AttendViewSet, SuscriptorViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter(trailing_slash=False)

from users.api import UsersViewSet
from auth.api import AuthViewSet

router.register('auth', AuthViewSet, base_name="auth")
router.register('users', UsersViewSet, base_name="users")
router.register('registro', AttendViewSet, base_name="registro")
router.register('suscriptores', SuscriptorViewSet, base_name="suscriptores")
