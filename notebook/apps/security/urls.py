from django.urls import path

from .views import TokenView

urlpatterns = [
    path(
        'login/',
        view=TokenView.as_view(),
        name='auth_login'
    ),
]
