from django.contrib.auth.models import User
from django.db import models

from .constants import PriorityTask, TaskStatusConstant


class BaseModel(models.Model):

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='created at'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='updated at'
    )

    class Meta:
        abstract = True


class UserTask(BaseModel):
    subject = models.CharField(
        max_length=100
    )
    description = models.TextField()
    status = models.IntegerField(
        default=TaskStatusConstant.CREATED.value
    )
    priority = models.IntegerField(
        default=PriorityTask.LOW.value
    )
    user_id = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name='tasks'
    )
    is_active = models.BooleanField(
        default=True
    )
