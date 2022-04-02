import pytest
from apps.notes.constants import PriorityTask, TaskStatusConstant
from apps.notes.models import UserTask
from apps.notes.services import UserTaskService
from mixer.backend.django import mixer
from rest_framework.exceptions import ValidationError


class TestDeleteTask:
    def test_delete_task_success(
        self,
        user_initial
    ):
        user = user_initial
        task = mixer.blend(
            UserTask,
            subject=mixer.faker.pystr(20),
            description=mixer.faker.pystr(20),
            priority=PriorityTask.MEDIUM.value,
            status=TaskStatusConstant.CREATED.value,
            user_id=user.pk
        )
        task_service = UserTaskService()
        task_service.validate_and_delete_task(
            user_id=user.pk,
            task_id=task.pk
        )

        task = UserTask.objects.get(pk=task.pk)
        assert not task.is_active

    def test_when_task_does_not_exists(
        self,
        user_initial
    ):
        user = user_initial
        task = mixer.blend(
            UserTask,
            subject=mixer.faker.pystr(20),
            description=mixer.faker.pystr(20),
            priority=PriorityTask.MEDIUM.value,
            status=TaskStatusConstant.CREATED.value,
            user_id=user.pk
        )
        task_service = UserTaskService()
        with pytest.raises(ValidationError) as e:
            task_service.validate_and_delete_task(
                user_id=user.pk,
                task_id=(task.pk + 1)
            )
        expected_data = {
            'component': 'task',
            'msg': 'task not found'
        }
        assert e.value.args[0] == expected_data

    def test_when_user_does_not_own_the_task(
        self,
        user_initial
    ):
        user = user_initial
        task = mixer.blend(
            UserTask,
            subject=mixer.faker.pystr(20),
            description=mixer.faker.pystr(20),
            priority=PriorityTask.MEDIUM.value,
            status=TaskStatusConstant.CREATED.value,
            user_id=user.pk
        )
        task_service = UserTaskService()
        with pytest.raises(ValidationError) as e:
            task_service.validate_and_delete_task(
                user_id=(user.pk + 1),
                task_id=task.pk
            )
        expected_data = {
            'component': 'task',
            'msg': 'the user does not own the task'
        }
        assert e.value.args[0] == expected_data
