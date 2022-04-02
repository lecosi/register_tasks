import pytest
from mixer.backend.django import mixer
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestGetToken:
    ENDPOINT = '/auth/login/'

    def test_get_token_success(
        self,
        user_initial
    ):
        user = user_initial
        client = APIClient()
        response = client.post(
            self.ENDPOINT,
            format='json',
            data=dict(
                username=user.username,
                password='123456'
            )
        )
        response_data = response.json()
        assert response.status_code == HTTP_200_OK
        assert response_data['access_token']
        assert response_data['refresh_token']
        assert response_data['expires']

    def test_when_username_is_invalid(self):
        client = APIClient()
        response = client.post(
            self.ENDPOINT,
            format='json',
            data=dict(
                username=mixer.faker.pystr(8),
                password='123456'
            )
        )
        expected_data = {
            'component': 'Authentication',
            'msg': 'username or password is incorrect'
        }
        response_data = response.json()
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response_data == expected_data

    def test_when_password_is_invalid(
        self,
        user_initial
    ):
        user = user_initial
        client = APIClient()
        response = client.post(
            self.ENDPOINT,
            format='json',
            data=dict(
                username=user.username,
                password=mixer.faker.pystr(8)
            )
        )
        expected_data = {
            'component': 'Authentication',
            'msg': 'username or password is incorrect'
        }
        response_data = response.json()
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response_data == expected_data

    def test_when_user_is_inactive(
        self,
        user_initial
    ):
        user = user_initial
        user.is_active = False
        user.save()

        client = APIClient()
        response = client.post(
            self.ENDPOINT,
            format='json',
            data=dict(
                username=user.username,
                password=mixer.faker.pystr(8)
            )
        )
        expected_data = {
            'component': 'Authentication',
            'msg': 'user is inactive'
        }
        response_data = response.json()
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response_data == expected_data

    def test_username_in_request_not_exists(
        self,
        user_initial
    ):
        client = APIClient()
        response = client.post(
            self.ENDPOINT,
            format='json',
            data=dict(
                password='123456'
            )
        )
        expected_data = {'username': ['This field is required.']}
        response_data = response.json()
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response_data == expected_data

    def test_password_in_request_not_exists(
        self,
        user_initial
    ):
        user = user_initial
        client = APIClient()
        response = client.post(
            self.ENDPOINT,
            format='json',
            data=dict(
                username=user.username
            )
        )
        expected_data = {'password': ['This field is required.']}
        response_data = response.json()
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response_data == expected_data
