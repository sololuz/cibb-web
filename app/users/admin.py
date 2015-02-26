# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm as UserCreationFormBase
from django.contrib.auth.forms import UserChangeForm as UserChangeFormBase
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

from users.models import User




class UserChangeForm(UserChangeFormBase):
	class Meta(UserChangeFormBase.Meta):
		model = User


class UserCreationForm(UserCreationFormBase):
	class Meta(UserCreationFormBase.Meta):
		model = User

	def clean_username(self):
		username = self.cleaned_data["username"]
		try:
			User.objects.get(username=username)
		except User.DoesNotExist:
			return username
		raise forms.ValidationError(self.error_messages['duplicate_username'])


class UserAdmin(AuthUserAdmin):
	form = UserChangeForm
	add_form = UserCreationForm


admin.site.register(User, UserAdmin)
