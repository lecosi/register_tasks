from django.contrib.auth.models import User

import pytest
from apps.security.pyjwt import JWTHandler
from apps.security.services import JWTAuthService
from mixer.backend.django import mixer
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN
)


@pytest.mark.django_db
class TestRefreshToken:
    ENDPOINT = '/auth/refresh_token/'

    def test_refresh_token_success(
        self,
        user_with_api_authenticated
    ):
        client, user, refresh_token = user_with_api_authenticated
        response = client.post(
            self.ENDPOINT,
            format='json',
            data=dict(
                refresh_token=refresh_token
            )
        )
        response_data = response.json()
        assert response.status_code == HTTP_200_OK
        assert response_data['access_token']
        assert response_data['refresh_token']
        assert response_data['expires']

    def test_refresh_token_invalid(
        self,
        user_with_api_authenticated
    ):
        client, user, _ = user_with_api_authenticated
        response = client.post(
            self.ENDPOINT,
            format='json',
            data=dict(
                refresh_token='test'
            )
        )
        expected_data = {
            'component': 'Authentication',
            'msg': 'Invalid token'
        }
        response_data = response.json()
        assert response.status_code == HTTP_403_FORBIDDEN
        assert response_data == expected_data

    def test_when_refresh_token_is_different_user(
        self,
        user_with_api_authenticated
    ):
        client, user, _ = user_with_api_authenticated

        user_2 = User.objects.create_user(
            username=mixer.faker.pystr(8),
            password=mixer.faker.pystr(8),
            is_active=True
        )
        jwr_handler = JWTHandler()
        jwt_auth_service = JWTAuthService(token_handler=jwr_handler)
        user_2_tokens = jwt_auth_service.create_token(
            user_id=user_2.pk
        )
        user_2_refresh_token = user_2_tokens['refresh_token']
        response = client.post(
            self.ENDPOINT,
            format='json',
            data=dict(
                refresh_token=user_2_refresh_token
            )
        )
        expected_data = {
            'component': 'Authentication',
            'msg': 'refresh token is invalid'
        }
        response_data = response.json()
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response_data == expected_data
