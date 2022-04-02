import time
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Union

from django.contrib.auth.models import User

from . import selectors as auth_sel
from .constants import TokenTypes
from .pyjwt import JWTHandler
from rest_framework.exceptions import PermissionDenied, ValidationError


class BaseAuthServices(ABC):

    @abstractmethod
    def create_token(self, customer_external_id):
        """Create an access authentication token
        it can be use by any encryption service, from a user.
        """

    @abstractmethod
    def validate_token(self, user: User, token: str):
        """This is a specific validation method for
        refresh access process, Validates an Invalid or
        Expire Signature of a token"""


class JWTAuthService(BaseAuthServices):

    def __init__(self, token_handler: JWTHandler):
        self.token_handler = token_handler

    @staticmethod
    def validate_user_can_get_token(
        *,
        username: str,
        password: str = None
    ) -> Optional[User]:

        user = auth_sel.get_user_by_username(
            username=username
        )

        if user is None:
            raise ValidationError({
                'component': 'Authentication',
                'msg': 'username or password is incorrect'
            })

        if not user.is_active:
            raise ValidationError({
                'component': 'Authentication',
                'msg': 'user is inactive'
            })

        if password is not None and not user.check_password(password):
            raise ValidationError({
                'component': 'Authentication',
                'msg': 'username or password is incorrect'
            })
        return user

    @staticmethod
    def get_expires_timestamp(
        *,
        minutes: int
    ) -> int:
        date = datetime.now()
        expires = date + timedelta(minutes=minutes)
        return int(time.mktime(expires.timetuple()))

    def create_token(
        self,
        *,
        user_id: int
    ) -> Dict[str, Any]:
        response = self._handle_tokens_creation(
            user_id=user_id
        )
        response['expires'] = self.get_expires_timestamp(
            minutes=TokenTypes.ACCESS.value
        )
        return response

    def validate_token(
        self,
        *,
        user: User,
        token: str
    ) -> Union[None]:
        payload = self.token_handler.decode(token=token)
        if user.pk != payload.get('user_id'):
            raise ValidationError({
                'component': 'Authentication',
                'msg': 'refresh token is invalid'
            })
        if payload.get('token_type') == TokenTypes.ACCESS.name:
            raise ValidationError({
                'component': 'Authentication',
                'msg': 'Not a refresh token'
            })

    def _handle_tokens_creation(self, user_id: int):
        response = {}
        self._validate_user_exists(user_id=user_id)

        token_lst = [
            {'token_type': 'ACCESS', 'name': 'access_token'},
            {'token_type': 'REFRESH', 'name': 'refresh_token'}
        ]

        for token_data in token_lst:
            params = {
                'user_id': user_id,
                'expires': self.get_expires_timestamp(
                    minutes=TokenTypes.ACCESS.value
                ),
                'token_type': token_data['token_type']
            }
            token = self.token_handler.encode(**params)
            response[token_data['name']] = token

        return response

    @staticmethod
    def _validate_user_exists(*, user_id: int) -> bool:
        filter_data = dict(id=user_id, is_active=True)
        user_qs = auth_sel.filter_user_by_params(params=filter_data)
        if not user_qs.exists():
            dict_response = dict(
                component='Authentication',
                msg='user not found',
            )
            raise PermissionDenied(dict_response)
        return True
