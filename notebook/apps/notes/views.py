from apps.notes.pagination import TaskInfoPagination
from apps.notes.serializers import (
    InputCreateTaskSerializer,
    InputPutTaskSerializer,
    OutputCreateTaskSerializer
)
from apps.notes.services import UserTaskService
from apps.security.authenticator import JWTAuthenticator
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT
)
from rest_framework.views import APIView


class TaskView(APIView):
    user_task_service = UserTaskService()
    input_serializer = InputCreateTaskSerializer
    output_serializer = OutputCreateTaskSerializer
    input_put_serializer = InputPutTaskSerializer

    authentication_classes = [JWTAuthenticator]
    pagination_class = TaskInfoPagination()

    def get(self, request):
        user = request.user
        response_data = self.user_task_service.get_task_data(
            user_id=user.pk
        )
        if not response_data:
            return Response(status=HTTP_200_OK)

        data = self.pagination_class.paginate_queryset(
            request=request,
            queryset=response_data
        )
        return Response(data, status=HTTP_200_OK)

    def post(self, request):
        input_serializer = self.input_serializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        user = request.user
        response_data = self.user_task_service.validate_and_create_task(
            user_id=user.id,
            **input_serializer.data
        )
        response = self.output_serializer(data=response_data)
        response.is_valid(raise_exception=True)
        return Response(response.data, status=HTTP_201_CREATED)

    def put(self, request, task_id):
        input_serializer = self.input_put_serializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        user = request.user
        self.user_task_service.validate_and_update_task(
            user_id=user.id,
            task_id=task_id,
            **input_serializer.data
        )
        return Response(status=HTTP_204_NO_CONTENT)

    def delete(self, request, task_id):
        user = request.user
        self.user_task_service.validate_and_delete_task(
            user_id=user.id,
            task_id=task_id
        )
        return Response(status=HTTP_204_NO_CONTENT)
