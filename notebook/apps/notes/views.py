from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT

from apps.notes.serializers import InputCreateTaskSerializer, \
    OutputCreateTaskSerializer
from apps.notes.services import UserTaskService


class TaskView(APIView):
    user_task_service = UserTaskService()
    input_serializer = InputCreateTaskSerializer
    output_serializer = OutputCreateTaskSerializer

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

