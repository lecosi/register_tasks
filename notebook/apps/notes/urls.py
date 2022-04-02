from django.urls import path

from .views import TaskView

urlpatterns = [
    path(
        '',
        view=TaskView.as_view(),
        name='get_task_list'
    ),
    path(
        'new/',
        view=TaskView.as_view(),
        name='create_task'
    ),
    path(
        '<int:task_id>/update/',
        view=TaskView.as_view(),
        name='update_task'
    ),
    path(
        '<int:task_id>/delete/',
        view=TaskView.as_view(),
        name='delete_task'
    ),
]
