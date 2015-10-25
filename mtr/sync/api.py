from rest_framework import viewsets
from rest_framework import serializers

from .model import Settings, Field


class SettingsSerializer(serializers.ModelSerializers):

    class Meta:
        model = Settings


class FieldSerializer(serializers.ModelSerializers):

    class Meta:
        model = Field


class SettingsAPIView(viewsets.ModelViewSet):
    queryset = Settings.objects.all()
    serializer_class = SettingsSerializer


class FieldAPIView(viewsets.ModelViewSet):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer
