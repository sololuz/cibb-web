# # -*- encoding:utf-8 -*-
import re
from django.core import validators
from django.core.exceptions import ValidationError
from rest_framework import serializers


class UsernameValidationMixin(object):
    def validate_username(self, value):
        validator = validators.RegexValidator(re.compile('^[\w.-]+$'), "invalid username", "invalid")

        try:
            validator(value)
        except ValidationError:
            raise serializers.ValidationError("Required. 255 characters or fewer. Letters, numbers "
                                              "and /./-/_ characters'")
        return value
