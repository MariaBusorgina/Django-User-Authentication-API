from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели пользователя."""

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def update(self, instance, validated_data):
        """Обновляет данные существующего пользователя на основе валидированных данных.

        Входные данные:
        - instance (User): Существующий объект пользователя.
        - validated_data (dict): Валидированные данные для обновления пользователя.

        Возвращает:
        - User: Обновленный объект пользователя.
        """
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        password = validated_data.get('password')
        if password:
            instance.set_password(password)
        instance.save()
        return instance



