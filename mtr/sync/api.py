from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, permissions, exceptions

from .model import Settings, Field


class SettingsSerializer(serializers.ModelSerializers):

    class Meta:
        model = Settings


class FieldSerializer(serializers.ModelSerializers):

    class Meta:
        model = Field
