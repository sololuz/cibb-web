"""
This module contains a domain logic for authentication
process. It called services because in DDD says it.

NOTE: Python doesn't have java limitations for "everytghing
should be contained in a class". Because of that, it
not uses clasess and uses simple functions.
"""
import uuid
from core.exceptions import WrongArguments

from django.apps import apps
from django.conf import settings
from django.db import transaction as tx
from django.db import IntegrityError
from django.utils.translation import ugettext as _

from djmail.template_mail import MagicMailBuilder

from users.serializers import UserSerializer

from .tokens import get_token_for_user
from .signals import user_registered as user_registered_signal


def send_register_email(user):
    """
    Given a user, send register welcome email
    message to specified user.
    """

    context = {
        "user": user,
        "base_url": settings.WEBSITE_BASE_URL,
    }
    mbuilder = MagicMailBuilder()
    email = mbuilder.registered_user(user.email, context)
    return bool(email.send())


def is_user_already_registered(username, email):
    """
    Checks if a specified user is already registred.

    Returns a tuple containing a boolean value that indicates if the user exists
    and in case he does whats the duplicated attribute
    """
    user_model = apps.get_model("users", "User")
    if user_model.objects.filter(username=username):
        return True, _("Username is already in use.")

    if user_model.objects.filter(email=email):
        return True, _("Email is already in use.")

    return False, None


@tx.atomic
def register(username, password, email, first_name, last_name):
    """
    Given a parsed parameters, try register a new user
    knowing that it follows a public register flow.

    This can raise `exc.IntegrityError` exceptions in
    case of conflics found.

    :returns: User
    """

    is_registered, reason = is_user_already_registered(username=username, email=email)
    if is_registered:
        raise WrongArguments(reason)

    user_model = apps.get_model("users", "User")
    user = user_model(username=username,
                      email=email,
                      first_name=first_name,
                      last_name=last_name,
                      )
    user.set_password(password)
    try:
        user.is_active = False
        user.is_staff = False
        user.token = str(uuid.uuid1())
        user.save()
    except IntegrityError:
        raise WrongArguments("User is already register.")

    send_register_email(user)
    user_registered_signal.send(sender=user.__class__, user=user)
    return user


def make_auth_response_data(user):
    """
    Given a domain and user, creates data structure
    using python dict containing a representation
    of the logged user.
    """
    serializer = UserSerializer(user)
    data = dict(serializer.data)
    data["auth_token"] = get_token_for_user(user, "authentication")
    return data
