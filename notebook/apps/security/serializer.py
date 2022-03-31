# Django
from rest_framework import serializers


class InputTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class OutTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
    expires = serializers.IntegerField()


class InputSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
