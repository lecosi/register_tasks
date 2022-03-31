from typing import Dict, Any, Optional

from django.contrib.auth.models import User
from django.db.models import QuerySet


def filter_user_by_params(
    *,
    params: Dict[str, Any]
) -> 'QuerySet[User]':
    return User.objects.filter(**params)


def get_user_by_username(
    *,
    username: str
) -> Optional[User]:

    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        return None
