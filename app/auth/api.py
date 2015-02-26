# -*- encodign:utf-8 -*-

import re
from auth.permissions import AuthPermissionSet
from auth.tokens import get_token_for_user
from core.exceptions import RequestValidationError, BadRequest, WrongArguments
from django.core.exceptions import ValidationError
from django.core.validators import validate_email, RegexValidator
from django.middleware import csrf

from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from djmail.template_mail import MagicMailBuilder

from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet

from users import User
from users.serializers import ConfirmRegisterSerializer
from users.services import get_and_validate_user

from .serializers import RegisterSerializer, EmailSerializer, UsernameSerializer

from .services import register
from .services import make_auth_response_data


class AuthViewSet(ViewSet):
    permission_classes = (AuthPermissionSet,)

    @list_route(methods=["POST"])
    def register(self, request, **kwargs):
        """
        Register for a new user.

        ---
        parameters:
            - name: first_name
              description: user first name
              required: true
              type: string
              paramType: form
            - name: last_name
              description: user last name
              required: true
              type: string
              paramType: form
            - name: email
              description: user email
              required: true
              type: string
              paramType: form
            - name: username
              description: username for the account
              required: true
              type: string
              paramType: form
            - name: password
              description: password
              required: true
              type: string
              paramType: form
        """
        if not settings.REGISTER_ENABLED:
            raise BadRequest(_("Public register is disabled."))

        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            raise RequestValidationError(serializer.errors)

        data = serializer.data
        register(**data)
        return Response(data, status=status.HTTP_201_CREATED)

    @list_route(methods=["POST"])
    def confirm_register(self, request):
        """
            Comfirmation account register.

                >>> register step required <<<
            ---
            parameters:
                - name: token
                  description: this token is sended to user email,
                               after user registration.
                  required: true
                  type: string
                  paramType: form
        """
        serializer = ConfirmRegisterSerializer(data=request.data)
        if not serializer.is_valid():
            raise WrongArguments(_("Missing arguments"))
        try:
            user = User.objects.get(token=serializer.data["token"])
        except User.DoesNotExist:
            raise WrongArguments(_("Token is invalid"))

        user.is_active = True
        mbuilder = MagicMailBuilder()
        cancel_token = get_token_for_user(user, "cancel_account")
        email = mbuilder.registered_user_confirmation(
            user.email, {
                "user": user,
                "cancel_token": cancel_token,
                "base_url": settings.WEBSITE_BASE_URL,
            })
        email.send()
        user.token = None
        user.save(update_fields=["is_active", "token"])

        return Response({
            "success": _("Welcome your account has been activated!"),
        }, status=status.HTTP_200_OK)

    @list_route(methods=["POST"])
    def login(self, request):
        """
        Login and authentication logic.
        """
        username = request.data.get('username', None)
        password = request.data.get('password', None)

        # This catch user name or email
        user = get_and_validate_user(username=username, password=password)
        data = make_auth_response_data(user)
        return Response(data, status=status.HTTP_200_OK)

    @list_route(methods=["GET"])
    def get_csrf_token(self, request):
        """
        Return de csrf token value for anymous or athenticated user
        """
        data = dict()
        data["csrf"] = csrf.get_token(request)
        return Response(data, status=status.HTTP_200_OK)

    @list_route(methods=["POST"])
    def check_email(self, request):
        """
        Validate the email availability.

        ---
        parameters:
            - name: email
              description: email a ser validado
              required: true
              type: string
              paramType: form
        """

        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.data['email']
        is_used_email = User.objects.filter(email=email).exists()

        if is_used_email:
            return Response({
                "used": _("Email is used another user"),
            }, status=status.HTTP_406_NOT_ACCEPTABLE, )
        else:
            return Response({
                "available": _("Email Available"),
            }, status=status.HTTP_202_ACCEPTED, )

    @list_route(methods=["POST"])
    def check_username(self, request):
        """
        Valida si un nombre de usuario esta disponible.

        ---
        parameters:
            - name: username
              description: username a validar
              required: true
              type: string
              paramType: form
        """
        serializer = UsernameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.data['username']
        is_used_username = User.objects.filter(username=username).exists()

        if is_used_username:
            return Response({
                "used": _("username is used another user"),
            }, status=status.HTTP_406_NOT_ACCEPTABLE, )
        else:
            return Response({
                "available": _("username Available"),
            }, status=status.HTTP_202_ACCEPTED, )


