from core.base.mixins import UsernameValidationMixin
from rest_framework import serializers

class BaseRegisterSerializer(UsernameValidationMixin, serializers.Serializer):
    first_name = serializers.CharField(max_length=256)
    last_name = serializers.CharField(max_length=256)
    email = serializers.EmailField(max_length=255)
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(min_length=4)

class RegisterSerializer(BaseRegisterSerializer):
    pass

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=200)

class UsernameSerializer(UsernameValidationMixin, serializers.Serializer):
    username = serializers.CharField(max_length=255)