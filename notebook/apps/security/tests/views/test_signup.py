import pytest
from django.contrib.auth.models import User
from mixer.backend.django import mixer
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestGetToken:
    ENDPOINT = '/auth/signup/'

    def test_signup_success(self):
        username = 'username'
        password = '123456'
        client = APIClient()
        response = client.post(
            self.ENDPOINT,
            format='json',
            data=dict(
                username=username,
                password=password
            )
        )
        user = User.objects.get(username=username)
        assert response.status_code == HTTP_201_CREATED
        assert user.is_active
        assert user.check_password(password)

    def test_when_username_already_exists(self):
        username = 'username'
        password = '123456'
        mixer.blend(
            User,
            username=username,
            is_active=True
        )
        client = APIClient()
        response = client.post(
            self.ENDPOINT,
            format='json',
            data=dict(
                username=username,
                password=password
            )
        )
        expected_data = {
            'component': 'SignUp',
            'msg': 'username already exists'
        }
        response_data = response.json()
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response_data == expected_data
