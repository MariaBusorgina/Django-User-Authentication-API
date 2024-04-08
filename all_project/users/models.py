from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserManager(BaseUserManager):

    def create_user(self, first_name, last_name, email, password=None, is_staff=False, is_superuser=False):
        if not email:
            raise ValueError("Введите почту пользователя")
        if not first_name:
            raise ValueError("Введите имя пользователя")
        if not last_name:
            raise ValueError("Введите фамилию пользователя")

        user = self.model(email=self.normalize_email(email))
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)
        user.is_active = True
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save()

        return user

    def create_superuser(self, first_name, last_name, email, password):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            is_staff=True,
            is_superuser=True
        )
        user.save()

        return user


class User(AbstractUser):
    first_name = models.CharField('Имя', max_length=255)
    last_name = models.CharField('Фамилия', max_length=255)
    email = models.EmailField('Почта', max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("first_name", "last_name")