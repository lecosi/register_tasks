# Django
from rest_framework import serializers

from .constants import PriorityTask


class InputCreateTaskSerializer(serializers.Serializer):
    subject = serializers.CharField()
    description = serializers.CharField()
    priority = serializers.ChoiceField(
        choices=[
            PriorityTask.LOW.value,
            PriorityTask.MEDIUM.value,
            PriorityTask.HIGH.value,
        ]
    )


class OutputCreateTaskSerializer(serializers.Serializer):
    task_id = serializers.IntegerField()


class OutTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
    expires = serializers.IntegerField()


class InputSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
