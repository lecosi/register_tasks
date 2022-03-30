import unittest

from mixer.backend.django import mixer
from rest_framework.exceptions import ValidationError

from notes.constants import PriorityTask, TaskStatusConstant
from notes.models import UserTask
from notes.services import TaskService


class TestUpdateTask(unittest.TestCase):
    def test_update_task_success(
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
        subject = mixer.faker.pystr(20)
        description = mixer.faker.pystr(20)
        priority = PriorityTask.HIGH.value
        status = TaskStatusConstant.IN_PROCESS.value

        task_service = TaskService()
        task_service.update_task(
            subject=subject,
            description=description,
            priority=priority,
            status=status,
            task_id=task.pk
        )

        task = UserTask.objects.get(pk=task.pk)
        self.assertEqual(task.subject, subject)
        self.assertEqual(task.description, description)
        self.assertEqual(task.priority, priority)
        self.assertEqual(task.status, status)

    def test_when_task_id_does_not_exists(
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
        subject = mixer.faker.pystr(20)
        description = mixer.faker.pystr(20)
        priority = PriorityTask.HIGH.value
        status = TaskStatusConstant.IN_PROCESS.value

        task_service = TaskService()
        with self.assertRaises(ValidationError) as context:
            task_service.update_task(
                subject=subject,
                description=description,
                priority=priority,
                status=status,
                task_id=(task.pk + 1)
            )
        assert 'task not found' in context.exception.detail['msg']

    def test_when_priority_is_invalid(
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
        subject = mixer.faker.pystr(20)
        description = mixer.faker.pystr(20)
        status = TaskStatusConstant.IN_PROCESS.value

        task_service = TaskService()
        with self.assertRaises(ValidationError) as context:
            task_service.update_task(
                subject=subject,
                description=description,
                priority=4,
                status=status,
                task_id=task.pk
            )
        assert 'task not found' in context.exception.detail['msg']

    def test_when_status_task_has_changed(
        self,
        mock_user
    ):
        user = mock_user
        subject = mixer.faker.pystr(20)
        description = mixer.faker.pystr(20)
        priority = PriorityTask.HIGH.value
        status = TaskStatusConstant.IN_PROCESS.value
        task = mixer.blend(
            UserTask,
            subject=subject,
            description=description,
            priority=priority,
            status=TaskStatusConstant.CREATED.value,
            user_id=user.pk
        )
        task_service = TaskService()
        task_service.update_task(
            subject=subject,
            description=description,
            priority=priority,
            status=status,
            task_id=task.pk
        )

        task = UserTask.objects.get(pk=task.pk)
        self.assertEqual(task.status, status)
