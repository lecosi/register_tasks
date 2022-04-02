# Django
from rest_framework import serializers


class InputCreateTaskSerializer(serializers.Serializer):
    subject = serializers.CharField()
    description = serializers.CharField()
    priority = serializers.IntegerField()


class OutputCreateTaskSerializer(serializers.Serializer):
    task_id = serializers.IntegerField()


class OutTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
    expires = serializers.IntegerField()


class InputSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class InputPutTaskSerializer(serializers.Serializer):
    subject = serializers.CharField()
    description = serializers.CharField()
    status = serializers.IntegerField()
    priority = serializers.IntegerField()
