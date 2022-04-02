from abc import ABC, abstractmethod
from typing import Dict, Optional, Union, List, Any

from django.db import transaction

from apps.notes import selectors as note_sel
from apps.notes.constants import PriorityTask, TaskStatusConstant
from apps.notes.models import UserTask
from apps.security import selectors as auth_sel
from rest_framework.exceptions import ValidationError


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
        task_id: int,
        user_id: int
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
        *,
        subject: str,
        description: str,
        priority: int,
        status: int,
        task_id: int,
        user_id: int
    ):
        task_qs = note_sel.filter_task_by_id(task_id=task_id)
        if not task_qs.exists():
            raise ValidationError({
                'component': 'task',
                'msg': 'task not found'
            })
        task = task_qs.last()
        is_owner = task.user_id == user_id
        if not is_owner:
            raise ValidationError({
                'component': 'task',
                'msg': 'the user does not own the task'
            })
        task_qs.update(
            subject=subject,
            description=description,
            priority=priority,
            status=status
        )

    def delete_task(
        self,
        task_id: int,
        user_id: int
    ) -> Union[None]:
        task_qs = note_sel.filter_task_by_id(task_id=task_id)
        if not task_qs.exists():
            raise ValidationError({
                'component': 'task',
                'msg': 'task not found'
            })
        task = task_qs.last()
        is_owner = task.user_id == user_id
        if not is_owner:
            raise ValidationError({
                'component': 'task',
                'msg': 'the user does not own the task'
            })

        task_qs.update(is_active=False)

    @staticmethod
    def validate_user_exists(
        *,
        user_id: int
    ) -> Union[None]:
        user_qs = auth_sel.filter_user_by_params(
            params=dict(id=user_id)
        )
        if not user_qs.exists():
            raise ValidationError({
                'component': 'task',
                'msg': 'user not found'
            })

    @staticmethod
    def validate_priority(
        *,
        priority: int
    ) -> Union[None]:
        try:
            PriorityTask(priority)
        except ValueError:
            raise ValidationError({
                'component': 'task',
                'msg': 'priority is invalid'
            })

    @staticmethod
    def validate_status_task(
        *,
        status_task: int
    ) -> Union[None]:
        try:
            TaskStatusConstant(status_task)
        except ValueError:
            raise ValidationError({
                'component': 'task',
                'msg': 'status is invalid'
            })

    @staticmethod
    def get_task_data_by_user(
        user_id: int
    ) -> 'QuerySet[UserTask]':
        return note_sel.filter_task_by_user_id(user_id=user_id).values(
            'id', 'subject', 'description', 'status', 'priority'
        )


class UserTaskService(TaskService):
    def __init__(self):
        super(TaskService, self).__init__()

    def validate_and_create_task(
        self,
        *,
        subject: str,
        description: str,
        priority: int,
        user_id: int
    ) -> Optional[Dict[str, int]]:
        self.validate_priority(priority=priority)
        self.validate_user_exists(user_id=user_id)
        task = self.create_task(
            subject=subject,
            description=description,
            priority=priority,
            user_id=user_id
        )
        data = dict(task_id=task.pk)
        return data

    def validate_and_update_task(
        self,
        *,
        subject: str,
        description: str,
        priority: int,
        status: int,
        task_id: int,
        user_id: int
    ) -> Union[None]:
        self.validate_priority(priority=priority)
        self.validate_user_exists(user_id=user_id)
        self.validate_status_task(status_task=status)
        self.update_task(
            subject=subject,
            description=description,
            priority=priority,
            status=status,
            task_id=task_id,
            user_id=user_id
        )

    def validate_and_delete_task(
        self,
        *,
        task_id: int,
        user_id: int
    ) -> Union[None]:
        self.validate_user_exists(user_id=user_id)
        self.delete_task(
            task_id=task_id,
            user_id=user_id
        )

    def get_task_data(
        self,
        user_id: int
    ) -> Optional[List[Dict[str, Any]]]:
        data_list = []
        task_list = self.get_task_data_by_user(user_id=user_id)
        for task in task_list:
            data = {
                'task_id': task['id'],
                'subject': task['subject'],
                'description': task['description'],
                'status_task': task['status'],
                'priority': task['priority'],
            }
            data_list.append(data)

        return data_list
