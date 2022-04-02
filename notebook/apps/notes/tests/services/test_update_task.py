import pytest
from apps.notes.constants import PriorityTask, TaskStatusConstant
from apps.notes.models import UserTask
from apps.notes.services import UserTaskService
from mixer.backend.django import mixer
from rest_framework.exceptions import ValidationError


class TestUpdateTask:
    def test_update_task_success(
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
        subject = mixer.faker.pystr(20)
        description = mixer.faker.pystr(20)
        priority = PriorityTask.HIGH.value
        status = TaskStatusConstant.IN_PROCESS.value

        task_service = UserTaskService()
        task_service.validate_and_update_task(
            subject=subject,
            description=description,
            priority=priority,
            status=status,
            task_id=task.pk,
            user_id=user.pk
        )

        task = UserTask.objects.get(pk=task.pk)
        assert task.subject == subject
        assert task.description == description
        assert task.priority == priority
        assert task.status == status

    def test_when_task_id_does_not_exists(
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
        subject = mixer.faker.pystr(20)
        description = mixer.faker.pystr(20)
        priority = PriorityTask.HIGH.value
        status = TaskStatusConstant.IN_PROCESS.value

        task_service = UserTaskService()
        with pytest.raises(ValidationError) as e:
            task_service.validate_and_update_task(
                subject=subject,
                description=description,
                priority=priority,
                status=status,
                task_id=(task.pk + 1),
                user_id=user.pk
            )

        expected_data = {
            'component': 'task',
            'msg': 'task not found'
        }
        assert e.value.args[0] == expected_data

    def test_when_priority_is_invalid(
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
        subject = mixer.faker.pystr(20)
        description = mixer.faker.pystr(20)
        status = TaskStatusConstant.IN_PROCESS.value

        task_service = UserTaskService()
        with pytest.raises(ValidationError) as e:
            task_service.validate_and_update_task(
                subject=subject,
                description=description,
                priority=4,
                status=status,
                task_id=task.pk,
                user_id=user.pk
            )

        expected_data = {
            'component': 'task',
            'msg': 'priority is invalid'
        }
        assert e.value.args[0] == expected_data

    def test_when_status_task_has_changed(
        self,
        user_initial
    ):
        user = user_initial
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
        task_service = UserTaskService()
        task_service.validate_and_update_task(
            subject=subject,
            description=description,
            priority=priority,
            status=status,
            task_id=task.pk,
            user_id=user.pk
        )

        task = UserTask.objects.get(pk=task.pk)
        assert task.status == status
