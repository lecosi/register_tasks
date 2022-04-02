from django.urls import path

from .views import RefreshTokenView, TokenView

urlpatterns = [
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
