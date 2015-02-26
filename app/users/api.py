
import uuid
from auth.tokens import get_user_for_token
from core.base.viewsets import ModelCrudViewSet
from core.exceptions import WrongArguments, NotAuthenticated, RequestValidationError

from django.db.models import Q
from django.middleware import csrf
from django.utils.translation import ugettext_lazy as _
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.conf import settings
from rest_framework.decorators import list_route

from rest_framework.response import Response
from rest_framework import status

from djmail.template_mail import MagicMailBuilder

from users.models import User
from users.permissions import UserPermissionSet
from users.serializers import (
    UserSerializer,
    PasswordChangeSerializer,
    AccountRecoverySerializer,
    PasswordRecoverySerializer,
    ChangeEmailSerializer, CancelAccountSerializer)



class UsersViewSet(ModelCrudViewSet):
    permission_classes = [UserPermissionSet, ]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    paginate_by = 25
    page_size = 25

    def list(self, request, *args, **kwargs):
        """
            List of all users
        """
        page = self.paginate_queryset(self.queryset)
        if page is not None:
            serializer = self.get_pagination_serializer(page)
        else:
            serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """
        Save the user  partial updates.

        We must detect if the user is trying to change his email so we can
        save that value and generate a token that allows him to validate it in
        the new email account
        """
        try:
            current_user = User.objects.get(id=kwargs["pk"])
        except Exception, e:
            raise RequestValidationError(_("User not found"))

        if current_user != request.user:
            raise RequestValidationError(_("You cann't change of other users information"))

        old_email = request.user.email
        new_email = request.data.get('email', None)

        if new_email is not None and new_email != old_email:
            valid_new_email = True
            duplicated_email = User.objects.filter(email=new_email).exists()

            try:
                validate_email(new_email)
            except ValidationError:
                valid_new_email = False

            if duplicated_email:
                raise WrongArguments(_("This mail is being used by another user"))
            elif not valid_new_email:
                raise WrongArguments(_("Not valid email"))

            # We need to generate a token for the email
            request.user.email_token = str(uuid.uuid1())
            request.user.new_email = new_email
            request.user.email = old_email
            request.data["email"] = old_email
            request.user.save(update_fields=["email_token", "new_email", "email"])

            mbuilder = MagicMailBuilder()
            email = mbuilder.change_email(
                request.user.email, {
                    "user": request.user,
                    "base_url": settings.WEBSITE_BASE_URL,
                })
            email.send()

        return super(UsersViewSet, self).partial_update(request, *args, **kwargs)

    @list_route(methods=["GET"])
    def profile(self, request):
        """
        Return the curren user profile

        """
        serializer = self.serializer_class
        if request.user.is_authenticated():
            return Response(serializer(request.user, context={}).data)
        else:
            return Response({'error': _('Authentication credentials were not provided')}, status=401)

    @list_route(methods=["POST"])
    def password_change(self, request):
        """
        Change current logged user password.
        ---
        serializer: PasswordChangeSerializer
        """

        serializer = PasswordChangeSerializer(data=request.DATA, instance=request.user)
        if serializer.is_valid():
            serializer.save()
            # TODO Send information email of password changed
            return Response({'success': _(u'Password successfully changed')}, status=200)
        return Response(serializer.errors, status=400)

    @list_route(methods=["POST"])
    def password_recovery(self, request):
        """
        Get a token to email for change password via token.
        ---
        serializer: AccountRecoverySerializer
        """
        username_or_email = request.data.get('username', None)

        if not username_or_email:
            raise WrongArguments(_("Invalid username or email"))

        try:
            queryset = User.objects.all()
            user = queryset.get(Q(username=username_or_email) | Q(email=username_or_email))
        except User.DoesNotExist:
            raise WrongArguments(_("Invalid username or email"))

        user.token = str(uuid.uuid1())
        user.save(update_fields=["token"])

        mbuilder = MagicMailBuilder()
        email = mbuilder.password_recovery(
            user.email, {
                "user": user,
                "base_url": settings.WEBSITE_BASE_URL,
            })
        email.send()

        return Response({
            "success": _("Mail sended successful!"),
            "email": user.email,
        }, status=status.HTTP_200_OK)

    @list_route(methods=["POST"])
    def password_from_recovery(self, request):
        """
        Change password with token
        >>> requiere password recovery step.<<<
        ---
        serializer: PasswordRecoverySerializer
        """
        serializer = PasswordRecoverySerializer(data=request.data)
        if not serializer.is_valid():
            raise WrongArguments(_("Missing arguments"))
        try:
            user = User.objects.get(token=serializer.data["token"])
        except User.DoesNotExist:
            raise WrongArguments(_("Token is invalid"))

        user.set_password(serializer.data["password"])
        user.token = None
        user.save(update_fields=["password", "token"])

        return Response({
            "success": _("Password Changed successfully!"),
        }, status=status.HTTP_200_OK)

    @list_route(methods=["POST"])
    def change_email(self, request):
        """
        Change the current logged user email change.
        ---
        serializer: ChangeEmailSerializer
        """
        serializer = ChangeEmailSerializer(data=request.data, many=False)
        if not serializer.is_valid():
            raise WrongArguments(_("Invalid, are you sure the token is correct and you didn't use it before?"))

        try:
            user = User.objects.get(email_token=serializer.data["email_token"])
        except User.DoesNotExist:
            raise WrongArguments(_("Invalid, are you sure the token is correct and you didn't use it before?"))

        user.email = user.new_email
        user.new_email = None
        user.email_token = None
        user.save(update_fields=["email", "new_email", "email_token"])

        return Response({
            "success": _("Email Changed successfully!"),
        }, status=status.HTTP_200_OK)


    # TODO get cancel token after create account
    @list_route(methods=["POST"])
    def cancel(self, request, pk=None):
        """
        Cancel an account via token.
        ---
        serializer: CancelAccountSerializer
        """
        serializer = CancelAccountSerializer(data=request.DATA, many=False)
        if not serializer.is_valid():
            raise WrongArguments(_("Missing arguments"))

        try:
            max_age_cancel_account = getattr(settings, "MAX_AGE_CANCEL_ACCOUNT", None)
            user = get_user_for_token(
                serializer.data["cancel_token"],
                "cancel_account",
                max_age=max_age_cancel_account
            )

        except NotAuthenticated:
            raise WrongArguments(_("Invalid, are you sure the token is correct?"))

        if not user.is_active:
            raise WrongArguments(_("Invalid, are you sure the token is correct?"))

        # user.delete() TODO Decide if account is cleared or disactivated only
        user.is_active = False
        user.save(update_fields=["is_active", ])

        return Response({
            "success": _("Your Accound has been cancelled!"),
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        Create a staff user.

            Funcion restringida a superusuarios.
        """
        return super(UsersViewSet, self).create(request)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific user.

            Restricted to super  users
        """
        return super(UsersViewSet, self).retrieve(request)

    def update(self, request, *args, **kwargs):
        """
        Update a specific user.

            Funcion restringida a superusuarios.
        """
        return super(UsersViewSet, self).update(request, *args, **kwargs)


    def destroy(self, request, *args, **kwargs):
        """
        Elimina a un usuario.

            Funcion restringida a superusuarios.
        """
        return super(UsersViewSet, self).destroy(request, *args, **kwargs)
    # @list_route(methods=["POST"])
    # def change_avatar(self, request):
    #     """
    #     Change avatar to current logged user.
    #     """
    #     self.check_permissions(request, "change_avatar", None)
    #
    #     avatar = request.FILES.get('avatar', None)
    #
    #     if not avatar:
    #         raise exc.WrongArguments(_("Incomplete arguments"))
    #
    #     try:
    #         pil_image(avatar)
    #     except Exception:
    #         raise exc.WrongArguments(_("Invalid image format"))
    #
    #     request.user.photo = avatar
    #     request.user.save(update_fields=["photo"])
    #     user_data = serializers.UserSerializer(request.user).data
    #
    #     return Response(user_data, status=status.HTTP_200_OK)
    #
    # @list_route(methods=["POST"])
    # def remove_avatar(self, request):
    #     """
    #     Remove the avatar of current logged user.
    #     """
    #     self.check_permissions(request, "remove_avatar", None)
    #     request.user.photo = None
    #     request.user.save(update_fields=["photo"])
    #     user_data = serializers.UserSerializer(request.user).data
    #     return Response(user_data, status=status.HTTP_200_OK)
    #
    # @detail_route(methods=["GET"])
    # def starred(self, request, pk=None):
    #     user = self.get_object()
    #     self.check_permissions(request, 'starred', user)
    #
    #     stars = votes_service.get_voted(user.pk, model=apps.get_model('projects', 'Project'))
    #     stars_data = StarredSerializer(stars, many=True)
    #     return Response(stars_data.data)
    #

