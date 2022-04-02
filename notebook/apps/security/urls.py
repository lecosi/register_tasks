from django.urls import path

from .views import RefreshTokenView, TokenView, SignUp

urlpatterns = [
    path(
        'signup/',
        view=SignUp.as_view(),
        name='auth_signup'
    ),
    path(
        'login/',
        view=TokenView.as_view(),
        name='auth_login'
    ),
    path(
        'refresh_token/',
        view=RefreshTokenView.as_view(),
        name='auth_refresh'
    ),
]
