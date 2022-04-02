from .authenticator import JWTAuthenticator
from .pyjwt import JWTHandler
from .serializers import (
    InputSerializer,
    InputSigUpSerializer,
    InputTokenSerializer,
    OutTokenSerializer
)
from .services import JWTAuthService, UserSignUp
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.views import APIView


class SignUp(APIView):
    input_serializer = InputSigUpSerializer
    signup_service = UserSignUp()

    def post(self, request):
        input_serializer = self.input_serializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        username = input_serializer.validated_data.get('username')
        password = input_serializer.validated_data.get('password')
        self.signup_service.create_user(
            username=username,
            password=password
        )
        return Response(status=HTTP_201_CREATED)


class TokenView(APIView):
    auth_service = JWTAuthService(
        token_handler=JWTHandler(),
    )
    input_serializer = InputTokenSerializer
    output_serializer = OutTokenSerializer

    def post(self, request):
        input_serializer = self.input_serializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        username = input_serializer.validated_data.get('username')
        password = input_serializer.validated_data.get('password')
        user = self.auth_service.validate_user_can_get_token(
            username=username,
            password=password
        )
        tokens = self.auth_service.create_token(
            user_id=user.pk
        )
        response = self.output_serializer(data=tokens)
        response.is_valid(raise_exception=True)
        return Response(response.data, status=HTTP_200_OK)


class RefreshTokenView(APIView):
    authentication_classes = [JWTAuthenticator]
    output_serializer = OutTokenSerializer

    def post(self, request):
        serializer = InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        auth_services = JWTAuthService(token_handler=JWTHandler())
        auth_services.validate_token(
            user=request.user,
            token=serializer.data.get('refresh_token')
        )
        tokens = auth_services.create_token(user_id=user.pk)
        response = self.output_serializer(data=tokens)
        response.is_valid(raise_exception=True)
        return Response(response.data)
