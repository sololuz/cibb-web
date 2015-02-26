# -*- encoding: utf-8 -*-

#Django imports
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy

#Third part imports
from allauth.socialaccount.views import SignupView as SignupViewBase
from allauth.socialaccount.views import LoginCancelledView as LoginCancelledViewBase
from allauth.socialaccount.views import LoginErrorView as LoginErrorViewBase
from allauth.socialaccount.views import ConnectionsView as ConnectionsViewBase

#Project imports
from socialaccount.forms import SignupForm, DisconnectForm

class SignupView(SignupViewBase):
    form_class = SignupForm
    template_name = 'socialaccount/signup.html'

signup = SignupView.as_view()

class LoginCancelledView(LoginCancelledViewBase):
    template_name = "socialaccount/login_cancelled.html"

login_cancelled = LoginCancelledView.as_view()

class LoginErrorView(LoginErrorViewBase):
    pass

login_error = LoginErrorView.as_view()

class ConnectionsView(ConnectionsViewBase):
    template_name = "socialaccount/connections.html"
    form_class = DisconnectForm
    success_url = reverse_lazy("socialaccount_connections")

connections = login_required(ConnectionsView.as_view())