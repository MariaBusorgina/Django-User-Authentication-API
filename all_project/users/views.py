from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import UserSerializer
from .services import user_find_by_email, create_token, CustomUserAuthentication


class RegisterApi(APIView):
    """Регистрация пользователя"""

    def post(self, request):
        """
        Регистрирует нового пользователя с переданными данными.

        Входные данные:
        - first_name: Имя пользователя.
        - last_name: Фамилия пользователя.
        - email: Электронная почта пользователя.
        - password: Пароль пользователя.

        Возвращает:
        Сериализованные данные нового пользователя.

        Raises:
        ValidationError: Если переданные данные недействительны.
        """
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        User.objects.create_user(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            password=data['password']
        )

        return Response(data=serializer.data)


class LoginApi(APIView):
    """Авторизация пользователя и создание JWT-токена"""

    def post(self, request):
        """
        Авторизует пользователя с переданными данными и создает JWT-токен.

        Входные данные:
        - email: Электронная почта пользователя.
        - password: Пароль пользователя.

        Возвращает:
        JWT-токен в виде куки "jwt".

        Raises:
        AuthenticationFailed: Если авторизация не удалась из-за неверных учетных данных.
        """
        email = request.data['email']
        password = request.data['password']

        user = user_find_by_email(email=email)

        if user is None:
            raise AuthenticationFailed("Invalid Credentials")

        if not user.check_password(password):
            raise AuthenticationFailed("Invalid Credentials")

        token = create_token(user_id=user.id)

        resp = Response()
        resp.set_cookie(key="jwt", value=token, httponly=True)

        return resp


class UserApi(APIView):
    """
    Данный эндпоинт может быть использован только если пользователь аутентифицирован.
    """
    authentication_classes = (CustomUserAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        """
        Получает данные аутентифицированного пользователя.

        Возвращает:
        Сериализованные данные пользователя.

        Raises:
        AuthenticationFailed: Если пользователь не аутентифицирован.
        """
        user = request.user

        serializer = UserSerializer(user)

        return Response(serializer.data)


class LogoutApi(APIView):
    """
    Данный эндпоинт может быть использован только если пользователь аутентифицирован.
    """
    authentication_classes = (CustomUserAuthentication, )
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        """
        Выход пользователя из системы и удаление JWT-токена.

        Удаляет куку "jwt".

        Возвращает:
        Сообщение об успешном удалении токена.

        Raises:
        AuthenticationFailed: Если пользователь не аутентифицирован.
        """
        resp = Response()
        resp.delete_cookie("jwt")
        resp.data = {"message": "Deleted"}

        return resp


class UserUpdateApi(APIView):
    """Обновление данных пользователя."""
    authentication_classes = [CustomUserAuthentication, ]

    def patch(self, request):
        """
        Пполное или частичное обновление данных пользователя.

        Параметры:
        - request: Запрос, содержащий данные для обновления пользователя.

        Возвращает:
        - Response: Возвращает обновленные данные пользователя, либо сообщение об ошибке в случае неверных данных.

        Коды статуса ответа:
        - 200: Успешное обновление данных пользователя.
        - 400: Ошибка валидации данных.
        """

        user = request.user
        data = request.data

        serializer = UserSerializer(user, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







