# -*- encoding: utf-8 -*-

#Django imports
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

#Third part imports
from allauth.socialaccount.forms import SignupForm as SignupFormBase
from allauth.socialaccount.forms import DisconnectForm as DisconnectFormBase
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Hidden, Submit

#Project imports
from barrio_chino.account.utils import PrependedIconText

SUBMIT_FORM_CLASSES = 'btn btn-lg btn-primary btn-block'

class SignupForm(SignupFormBase):
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = reverse_lazy('socialaccount_signup')
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            HTML('<hr>'),
            PrependedIconText('username', placeholder=_('Username'), icon_class="fa fa-user"),
            PrependedIconText('email', placeholder=_('Email'), icon_class="fa fa-envelope"),
            Hidden('next', value=''),
            HTML('<hr>'),
            Submit('submit', _('Sign Up'),
                   css_class=SUBMIT_FORM_CLASSES),
            HTML('</br>'),
        )


class DisconnectForm(DisconnectFormBase):
    pass