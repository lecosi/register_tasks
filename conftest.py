import pytest
from django.contrib.auth.models import User
from mixer.backend.django import mixer


@pytest.fixture
def user_initial(db) -> User:
    user = User.objects.create_user(
        username=mixer.faker.pystr(8),
        password='123456',
        is_active=True
    )
    return user

