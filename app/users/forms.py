# -*- coding: utf-8 -*-

#Django imports
from .utils import PrependedIconText, CustomCheckbox
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Hidden, Submit
from django import forms
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _





#Third part imports
from allauth.account.forms import SignupForm as SignupFormBase
from allauth.account.forms import LoginForm as LoginFormBase

# Project imports
from .cibb.users.models.models import User



SUBMIT_FORM_CLASSES = 'btn btn-lg btn-primary btn-block'
USERNAME = 'username'
EMAIL = 'email'
USERNAME_EMAIL = 'username_email'


class UserForm(forms.ModelForm):

    class Meta:
        # Set this form to use the User model.
        model = User

        # Constrain the UserForm to just these fields.
        fields = ("first_name", "last_name")


class LoginForm(LoginFormBase):
    """
    Form for authenticating users.
    """
    # remember_me = forms.BooleanField(initial=False, required=False)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        if settings.ACCOUNT_AUTHENTICATION_METHOD == USERNAME:
            self.fields['login'].label = _('Username')
        elif settings.ACCOUNT_AUTHENTICATION_METHOD == EMAIL:
            self.fields['login'].label = _('Email')
        elif settings.ACCOUNT_AUTHENTICATION_METHOD == USERNAME_EMAIL:
            self.fields['login'].label = _('Username or Email')

        self.helper = FormHelper(self)
        self.helper.form_action = reverse_lazy('account_login')
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            PrependedIconText('login', placeholder=_('Username'), icon_class="fa fa-user"),
            PrependedIconText('password', placeholder=_('Password'), icon_class="fa fa-lock", css_class="login-pass"),
            CustomCheckbox('remember', placeholder=_('Remember me'), type_checkbox="checkbox-primary"),
            Hidden('next', value=''),
            Submit('submit', _('Sign In'),
                   css_class=SUBMIT_FORM_CLASSES),
        )

class SignupForm(SignupFormBase):
    """A form for creating new users in the Frontend Site. Includes all the required
    fields, plus a repeated password and email confirmation. here add more custom fields"""

    # TODO Arreglar los  demas campos como sexo, u otros por revisar.

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = ''
        self.helper.form_class = 'user-form'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('username', placeholder=_('Username'),),
            Field('first_name', placeholder=_('first name'),),
            Field('last_name', label=_('last name'), placeholder=_('last name'),),
            Field('email', placeholder=_('Email'),),
            Field('gender', _('Gender')),
            Field('password1', placeholder=_('Password'),),
            Field('password2', placeholder=_('Password confirmation'),),
            Submit('submit', _('Create Account'), css_class=SUBMIT_FORM_CLASSES),
        )

    class Meta:
        fields = ('username', 'first_name', 'last_name', 'email',
                  'gender', 'password1', 'password2',)