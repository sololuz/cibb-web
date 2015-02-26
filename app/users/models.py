# -*- encoding:utf-8 -*-

# Python imports

# Django imports
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

# Third part imports

# Project imports
from core.utils import date
from .config import EMAIL_CONFIRMATION, REQUIRED_FIELDS, password_changed
from core.base.models import BaseDate

SEX_CHOICES = (
    ('M', _('male')),
    ('F', _('female'))
)


class User(AbstractUser):
    """
        User Profile Model
        Contains personal info of a user
    """
    # custom fields
    about = models.TextField(_('about me'), blank=True)
    gender = models.CharField(_('gender'), max_length=1, choices=SEX_CHOICES, blank=True)
    birth_date = models.DateField(_('birth date'), blank=True, null=True)
    address = models.CharField(_('address'), max_length=150, blank=True)
    city = models.CharField(_('city'), max_length=30, blank=True)
    country = models.CharField(_('country'), max_length=30, blank=True)

    new_email = models.EmailField(_('new email address'), null=True, blank=True)
    email_token = models.CharField(max_length=200, null=True, blank=True, default=None, verbose_name=_("email token"))
    token = models.CharField(max_length=200, null=True, blank=True, default=None,
                             verbose_name=_("token"))

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = REQUIRED_FIELDS

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __unicode__(self):
        return self.username

    def save(self, *args, **kwargs):
        """ ensure instance has usable password when created """
        if not self.pk and self.has_usable_password() is False:
            self.set_password(self.password)

        super(User, self).save(*args, **kwargs)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def add_email(self):
        """
        Add email to DB and sends a confirmation mail if PROFILE_EMAL_CONFIRMATION is True
        """
        if EMAIL_CONFIRMATION:
            from . import EmailAddress
            self.is_active = False
            self.save()
            EmailAddress.objects.add_email(self, self.email)
            return True
        else:
            return False

    def change_password(self, new_password):
        """
        Changes password and sends a signal
        """
        self.set_password(new_password)
        self.save()
        password_changed.send(sender=self.__class__, user=self)

    def get_absolute_url(self):
        return "/api/users/%i/" % self.id


class SocialLink(BaseDate):
    """
    External links like website or social network profiles
    """
    user = models.ForeignKey(User, verbose_name=_('user'))
    url = models.URLField(_('url'))
    description = models.CharField(_('description'), max_length=128, blank=True)

    class Meta:
        app_label = 'profiles'
        db_table = 'profiles_social_links'
        unique_together = ('user', 'url')

    def __unicode__(self):
        return self.url

