from typing import Tuple

import pytest
from django.contrib.auth.models import User
from mixer.backend.django import mixer
from rest_framework.test import APIClient

from apps.security.pyjwt import JWTHandler
from apps.security.services import JWTAuthService


@pytest.fixture
def user_initial(db) -> User:
    user = User.objects.create_user(
        username=mixer.faker.pystr(8),
        password='123456',
        is_active=True
    )
    return user


@pytest.fixture
def user_with_api_authenticated(db) -> Tuple[APIClient, User, str]:
    user = User.objects.create_user(
        username=mixer.faker.pystr(8),
        password='123456',
        is_active=True
    )
    jwr_handler = JWTHandler()
    jwt_auth_service = JWTAuthService(token_handler=jwr_handler)
    tokens = jwt_auth_service.create_token(
        user_id=user.id
    )
    access_token = tokens['access_token']
    refresh_token = tokens['refresh_token']

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token: ' + access_token)
    return client, user, refresh_token
