from abc import ABC, abstractmethod
from typing import Optional, Union, Dict

from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.notes.constants import PriorityTask
from apps.notes.models import UserTask
from apps.security import selectors as auth_sel


class NoteMethod(ABC):

    @abstractmethod
    def create_task(
        self,
        subject: str,
        description: str,
        priority: int,
        user_id: int
    ):
        """creates a task on an initial state and make
        initial validations"""

    @abstractmethod
    def update_task(
        self,
        subject: str,
        description: str,
        priority: int,
        status: int,
        task_id: int
    ):
        """update a task and make validations"""

    @abstractmethod
    def delete_task(
        self,
        task_id: int,
        user_id: int
    ):
        """delete a task and make validations"""


class TaskService(NoteMethod):

    @staticmethod
    def validate_create_task(
        *,
        priority: int,
        user_id: int
    ) -> Union[None]:
        user_qs = auth_sel.filter_user_by_params(
            params=dict(id=user_id)
        )
        if not user_qs.exists():
            raise ValidationError({
                'component': 'create task',
                'msg': 'user not found'
            })
        try:
            PriorityTask[priority]
        except ValueError:
            raise ValidationError({
                'component': 'create task',
                'msg': 'priority is invalid'
            })

    @transaction.atomic
    def create_task(
        self,
        subject: str,
        description: str,
        priority: int,
        user_id: int
    ) -> Optional[UserTask]:
        return UserTask.objects.create(
            subject=subject,
            description=description,
            priority=priority,
            user_id=user_id
        )

    def update_task(
        self,
        subject: str,
        description: str,
        priority: int,
        status: int,
        task_id: int
    ):
        pass

    def delete_task(
        self,
        task_id: int,
        user_id: int
    ):
        pass

    def get_task_lst_by_user_id(
        self,
        user_id: int
    ):
        pass


class UserTaskService(TaskService):
    def __init__(self):
        super(TaskService, self).__init__()

    def validate_and_create_task(
        self,
        subject: str,
        description: str,
        priority: int,
        user_id: int
    ) -> Optional[Dict[str, int]]:
        self.validate_create_task(
            priority=priority,
            user_id=user_id
        )
        task = self.create_task(
            subject=subject,
            description=description,
            priority=priority,
            user_id=user_id
        )
        data = dict(task_id=task.pk)
        return data
