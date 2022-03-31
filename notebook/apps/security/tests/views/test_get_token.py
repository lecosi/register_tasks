import pytest
from rest_framework.test import APIClient
from rest_framework.status import HTTP_200_OK


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
