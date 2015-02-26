import hashlib

from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from users.models import User

PASSWORD_MAX_LENGTH = User._meta.get_field('password').max_length


class UserSerializer(serializers.ModelSerializer):
    """ Profile Serializer for visualization """
    url = serializers.URLField(source='get_absolute_url', read_only=True, )

    # avatar = serializers.SerializerMethodField('get_avatar')
    # location = serializers.SerializerMethodField('get_location')
    # social_links_url = serializers.HyperlinkedIdentityField(lookup_field='username', view_name='api_user_social_links_list')
    # social_links = SocialLinkSerializer(source='sociallink_set', many=True, read_only=True)

    def get_avatar(self, obj):
        """ avatar from gravatar.com """
        return 'https://www.gravatar.com/avatar/%s' % hashlib.md5(obj.email).hexdigest()

    def get_location(self, obj):
        """ return user's location """
        if not obj.city and not obj.country:
            return None
        elif obj.city and obj.country:
            return '%s, %s' % (obj.city, obj.country)
        elif obj.city or obj.country:
            return obj.city or obj.country

    class Meta:
        model = User
        fields = [
            'url',
            'username',
            'first_name',
            'last_name',
            'email',
            'about',
            'gender',
            'birth_date',
            'address',
            'city',
            'date_joined',
            'last_login',
        ]

        read_only_fields = (
            'username',
            'date_joined',
            'last_login'
        )


class PasswordChangeSerializer(serializers.Serializer):
    """
    Change password serializer
    """
    current_password = serializers.CharField(
        help_text=_('Current Password'),
        max_length=PASSWORD_MAX_LENGTH,
        required=False  # optional because users subscribed from social network won't have a password set
    )
    password1 = serializers.CharField(
        help_text=_('New Password'),
        max_length=PASSWORD_MAX_LENGTH
    )
    password2 = serializers.CharField(
        help_text=_('New Password (confirmation)'),
        max_length=PASSWORD_MAX_LENGTH
    )

    def update(self, instance, validated_data):
        """ change password """
        if instance is not None:
            instance.change_password(validated_data.get('password2'))
        return instance

    def create(self, validated_data):
        return User(**validated_data)

    def validate_current_password(self, value):
        """
        current password check
        """
        if self.instance.has_usable_password() and not self.instance.check_password(value):
            raise serializers.ValidationError(_('Current password is not correct'))
        return value

    def validate(self, data):
        """
        password_confirmation check
        """
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(_('Password confirmation mismatch'))
        return data


class PasswordRecoverySerializer(serializers.Serializer):
    token = serializers.CharField(max_length=200)
    password = serializers.CharField(min_length=6)

class AccountRecoverySerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)

class ConfirmRegisterSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=200)

class ChangeEmailSerializer(serializers.Serializer):
    email_token = serializers.CharField(max_length=200)


class CancelAccountSerializer(serializers.Serializer):
    cancel_token = serializers.CharField(max_length=200)
