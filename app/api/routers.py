# -*- encoding:utf-8 -*-
from registro.api import (
    AttendViewSet,
    SuscriptorViewSet,
    ContactViewSet,
    SpeakerViewSet,
    StaffViewSet,
    SponsorViewSet,
)

from rest_framework.routers import DefaultRouter


router = DefaultRouter(trailing_slash=False)

from users.api import UsersViewSet
from auth.api import AuthViewSet

router.register('auth', AuthViewSet, base_name="auth")
router.register('users', UsersViewSet, base_name="users")
router.register('registro', AttendViewSet, base_name="registro")
router.register('suscriptors', SuscriptorViewSet, base_name="suscriptores")
router.register('contacts', ContactViewSet, base_name="contactos")
router.register('speakers', SpeakerViewSet, base_name="speakers")
router.register('staff', StaffViewSet, base_name="staff")
router.register('sponsors', SponsorViewSet, base_name="sponsors")
