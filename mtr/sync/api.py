from rest_framework import generics
from rest_framework.response import Response
from rest_framework import serializers, exceptions

from .model import Settings, Field


class SettingsSerializer(serializers.ModelSerializers):

    class Meta:
        model = Settings


class FieldSerializer(serializers.ModelSerializers):

    class Meta:
        model = Field


class SettingsAPIView(generics.ListCreateAPIView):
    pass


class FieldAPIView(generics.ListCreateAPIView):
    pass
