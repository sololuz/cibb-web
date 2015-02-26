
"""
This model contains a domain logic for users application.
"""
from core.exceptions import WrongArguments

from django.apps import apps
from django.db.models import Q
from django.conf import settings



from core.utils.urls import get_absolute_url
from core.utils.gravatar import get_gravatar_url


def get_and_validate_user(username, password):
    """
    Check if user with username/email exists and specified
    password matchs well with existing user password.

    if user is valid,  user is returned else, corresponding
    exception is raised.
    """
    user_model = apps.get_model("users", "User")
    qs = user_model.objects.filter(Q(username=username) |
                                   Q(email=username))
    if len(qs) == 0:
        raise WrongArguments("Username or password does not matches user.")

    user = qs[0]
    if not user.check_password(password):
        raise WrongArguments("Username or password does not matches user.")

    return user



# def get_photo_url(photo):
#     """Get a photo absolute url and the photo automatically cropped."""
#     try:
#         url = get_thumbnailer(photo)['avatar'].url
#         return get_absolute_url(url)
#     except InvalidImageFormatError as e:
#         return None
#
#
# def get_photo_or_gravatar_url(user):
#     """Get the user's photo/gravatar url."""
#     if user:
#         return get_photo_url(user.photo) if user.photo else get_gravatar_url(user.email)
#     return ""
#
#
# def get_big_photo_url(photo):
#     """Get a big photo absolute url and the photo automatically cropped."""
#     try:
#         url = get_thumbnailer(photo)['big-avatar'].url
#         return get_absolute_url(url)
#     except InvalidImageFormatError as e:
#         return None
#
#
# def get_big_photo_or_gravatar_url(user):
#     """Get the user's big photo/gravatar url."""
#     if user:
#         return get_big_photo_url(user.photo) if user.photo else get_gravatar_url(user.email, size=settings.DEFAULT_BIG_AVATAR_SIZE)
#     return ""
