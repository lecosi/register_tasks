import unittest

from mixer.backend.django import mixer
from notebook.apps.notes.constants import PriorityTask, TaskStatusConstant
from notebook.apps.notes.models import UserTask
from notebook.apps.notes.services import TaskService
from rest_framework.exceptions import ValidationError


class TestDeleteTask(unittest.TestCase):
    def test_delete_task_success(
        self,
        mock_user
    ):
        user = mock_user
        task = mixer.blend(
            UserTask,
            subject=mixer.faker.pystr(20),
            description=mixer.faker.pystr(20),
            priority=PriorityTask.MEDIUM.value,
            status=TaskStatusConstant.CREATED.value,
            user_id=user.pk
        )
        task_service = TaskService()
        task_service.delete_task(
            user_id=user.pk,
            task_id=task.pk
        )

        task = UserTask.objects.get(pk=task.pk)
        self.assertEqual(task.is_active, False)

    def test_when_user_does_not_exists(
        self,
        mock_user
    ):
        user = mock_user
        task = mixer.blend(
            UserTask,
            subject=mixer.faker.pystr(20),
            description=mixer.faker.pystr(20),
            priority=PriorityTask.MEDIUM.value,
            status=TaskStatusConstant.CREATED.value,
            user_id=user.pk
        )
        task_service = TaskService()
        with self.assertRaises(ValidationError) as context:
            task_service.delete_task(
                user_id=(user.pk + 1),
                task_id=task.pk
            )
        assert 'user not found' in context.exception.detail['msg']

    def test_when_task_does_not_exists(
        self,
        mock_user
    ):
        user = mock_user
        task = mixer.blend(
            UserTask,
            subject=mixer.faker.pystr(20),
            description=mixer.faker.pystr(20),
            priority=PriorityTask.MEDIUM.value,
            status=TaskStatusConstant.CREATED.value,
            user_id=user.pk
        )
        task_service = TaskService()
        with self.assertRaises(ValidationError) as context:
            task_service.delete_task(
                user_id=user.pk,
                task_id=(task.pk + 1)
            )
        assert 'task not found' in context.exception.detail['msg']
