from registro.models import Attend, Suscriptor
from rest_framework import serializers


class AttendSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attend


class SuscriptorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Suscriptor
