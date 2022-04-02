from django.db.models import QuerySet

from apps.notes.models import UserTask


def filter_task_by_id(
    *,
    task_id: int
) -> 'QuerySet[UserTask]':
    return UserTask.objects.filter(
        id=task_id
    )
