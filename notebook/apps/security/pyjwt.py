# Standard Library
import logging

# Django
from django.conf import settings

# Libraries
import jwt
from rest_framework.exceptions import AuthenticationFailed

logger = logging.getLogger(__name__)


class JWTHandler:

    @staticmethod
    def get_secret_key():
        return settings.SECRET_KEY

    def encode(
        self,
        *,
        user_id: str,
        expires: int,
        token_type: str,
        algorithm: str = 'HS256'
    ) -> str:
        secret_key = self.get_secret_key()
        payload = {
            'user_id': user_id,
            'exp': expires,
            'token_type': token_type
        }

        token = jwt.encode(
            payload,
            secret_key,
            algorithm=algorithm,
        )

        return token

    def decode(
        self,
        *,
        token: str,
        algorithm: str = 'HS256'
    ):
        secret_key = self.get_secret_key()
        try:
            payload = jwt.decode(token, secret_key, algorithms=algorithm)
            return payload
        except (jwt.DecodeError, jwt.InvalidSignatureError):
            raise AuthenticationFailed({
                'component': 'Authentication',
                'msg': 'Invalid token'
            })
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed({
                'component': 'Authentication',
                'msg': 'expired token'
            })
