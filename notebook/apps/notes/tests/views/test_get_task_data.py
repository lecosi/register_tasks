import pytest
from apps.notes.constants import PriorityTask, TaskStatusConstant
from apps.notes.models import UserTask
from mixer.backend.django import mixer
from rest_framework.status import HTTP_200_OK


@pytest.mark.django_db
class TestGetTaskData:
    ENDPOINT = '/tasks/'

    def test_get_task_data_success(
        self,
        user_with_api_authenticated
    ):
        client, user, _ = user_with_api_authenticated

        mixer.blend(
            UserTask,
            subject=mixer.faker.pystr(20),
            description=mixer.faker.pystr(20),
            priority=PriorityTask.MEDIUM.value,
            status=TaskStatusConstant.CREATED.value,
            user_id=user.pk,
            is_active=True
        )
        response = client.get(
            self.ENDPOINT,
            format='json'
        )
        response_data = response.json()
        assert response.status_code == HTTP_200_OK
        assert len(response_data) == 1
