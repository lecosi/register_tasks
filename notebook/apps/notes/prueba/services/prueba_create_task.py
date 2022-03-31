import unittest

from mixer.backend.django import mixer
from notebook.apps.notes.constants import PriorityTask
from notebook.apps.notes.services import TaskService
from rest_framework.exceptions import ValidationError


class TestCreateTask(unittest.TestCase):
    def test_create_task_success(
        self,
        mock_user
    ):
        user = mock_user
        task_service = TaskService()
        subject = mixer.faker.pystr(20)
        description = mixer.faker.pystr(20)
        priority = PriorityTask.LOW.value

        task = task_service.create_task(
            subject=subject,
            description=description,
            priority=priority,
            user_id=user.pk
        )
        self.assertEqual(task.subject, subject)
        self.assertEqual(task.description, description)
        self.assertEqual(task.priority, priority)
        self.assertEqual(task.user_id, user.pk)

    def test_when_user_does_not_exists(
        self,
        mock_user
    ):
        user = mock_user
        task_service = TaskService()
        subject = mixer.faker.pystr(20)
        description = mixer.faker.pystr(20)
        priority = PriorityTask.LOW.value

        with self.assertRaises(ValidationError) as context:
            task_service.create_task(
                subject=subject,
                description=description,
                priority=priority,
                user_id=(user.pk + 1)
            )
        assert 'customer not found' in context.exception.detail['msg']

    def test_when_priority_is_invalid(
        self,
        mock_user
    ):
        user = mock_user
        task_service = TaskService()
        subject = mixer.faker.pystr(20)
        description = mixer.faker.pystr(20)

        with self.assertRaises(ValidationError) as context:
            task_service.create_task(
                subject=subject,
                description=description,
                priority=4,
                user_id=user.pk
            )
        assert 'priority is invalid' in context.exception.detail['msg']
