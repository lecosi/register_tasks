import pytest
from apps.notes.constants import PriorityTask
from apps.notes.models import UserTask
from apps.notes.services import UserTaskService
from mixer.backend.django import mixer
from rest_framework.exceptions import ValidationError


@pytest.mark.django_db
class TestCreateTask:
    def test_create_task_success(
        self,
        user_initial
    ):
        user = user_initial
        task_service = UserTaskService()
        subject = mixer.faker.pystr(20)
        description = mixer.faker.pystr(20)
        priority = PriorityTask.LOW.value

        task_service.validate_and_create_task(
            subject=subject,
            description=description,
            priority=priority,
            user_id=user.pk
        )
        task = UserTask.objects.filter(user_id=user.pk).last()
        assert task.subject == subject
        assert task.description == description
        assert task.priority == priority
        assert task.user.pk == user.pk

    def test_when_user_does_not_exists(
        self,
        user_initial
    ):
        user = user_initial
        task_service = UserTaskService()
        subject = mixer.faker.pystr(20)
        description = mixer.faker.pystr(20)
        priority = PriorityTask.LOW.value

        user_id_fake = (user.pk + 1)

        with pytest.raises(ValidationError) as e:
            task_service.validate_and_create_task(
                subject=subject,
                description=description,
                priority=priority,
                user_id=user_id_fake
            )

        expected_data = {
            'component': 'task',
            'msg': 'user not found'
        }
        assert e.value.args[0] == expected_data

    def test_when_priority_is_invalid(
        self,
        user_initial
    ):
        user = user_initial
        task_service = UserTaskService()
        subject = mixer.faker.pystr(20)
        description = mixer.faker.pystr(20)
        priority_fake = 4
        with pytest.raises(ValidationError) as e:
            task_service.validate_and_create_task(
                subject=subject,
                description=description,
                priority=priority_fake,
                user_id=user.pk
            )

        expected_data = {
            'component': 'task',
            'msg': 'priority is invalid'
        }
        assert e.value.args[0] == expected_data
