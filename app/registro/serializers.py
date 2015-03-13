from registro.models import Attend, Suscriptor, Contact
from rest_framework import serializers


class AttendSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attend


class SuscriptorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Suscriptor

class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact