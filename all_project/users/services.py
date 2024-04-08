import datetime
import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from all_project.settings import JWT_SECRET
from users.models import User


def user_find_by_email(email):
    """Поиск пользователя по адресу электронной почты"""
    user = User.objects.filter(email=email).first()
    return user


def create_token(user_id):
    """Создание JWT-токена"""
    payload = dict(
        id=user_id,
        exp=datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        iat=datetime.datetime.utcnow()
    )
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

    return token


class CustomUserAuthentication(BaseAuthentication):
    """Проверка аутентификации пользователя"""

    def authenticate(self, request):
        token = request.COOKIES.get("jwt")

        if not token:
            return None

        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        except:
            raise AuthenticationFailed("Unauthorized")

        user = User.objects.filter(id=payload["id"]).first()

        return (user, None)