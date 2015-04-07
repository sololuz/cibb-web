from registro.models import Attend, Suscriptor, Contact, Speaker, Staff, Sponsor
from rest_framework import serializers
from sorl.thumbnail.shortcuts import get_thumbnail
from django.conf import settings

class AttendSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attend


class SuscriptorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Suscriptor

class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact

class SpeakerSerializer(serializers.ModelSerializer):

    photo =  serializers.SerializerMethodField()

    def get_photo(self, obj):
        try:
            # ancho x alto
            return  "%s%s"%( settings.WEBSITE_BASE_URL, get_thumbnail(
            obj.photo,'500x550', crop='center', upscale=True, quality=99).url)

        except Exception, e:
            return ""

    class Meta:
        model = Speaker

class StaffSerializer(serializers.ModelSerializer):
    photo =  serializers.SerializerMethodField()

    def get_photo(self, obj):
        try:

            return  "%s%s"%( settings.WEBSITE_BASE_URL, get_thumbnail(
            obj.photo,'550x600', crop='center', upscale=True, quality=99).url)

        except Exception, e:
            return ""
    class Meta:
        model = Staff

class SponsorSerializer(serializers.ModelSerializer):
    logo =  serializers.SerializerMethodField()

    def get_logo(self, obj):
        try:

            return  "%s%s"%( settings.WEBSITE_BASE_URL, get_thumbnail(
            obj.logo,'250x150', crop='center', upscale=True, quality=99).url)

        except Exception, e:
            return ""
    class Meta:
        model = Sponsor