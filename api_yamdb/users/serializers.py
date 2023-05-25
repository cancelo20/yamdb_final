import re

from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

from .models import User


ROLE_CHOICES = User.ROLE_CHOICES


class RegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации."""

    username = serializers.CharField(
        max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    email = serializers.EmailField(
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    class Meta:
        model = User
        fields = ('username', 'email')
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(), fields=['username', 'email']
            )
        ]

    def validate(self, attrs):
        username = attrs.get('username')

        if username.lower() == 'me':
            raise ValidationError('Использовано служебное имя')

        reg = re.compile(r'^[\w.@+-]+')

        if not reg.match(username):
            raise ValidationError('Доступные символы: A-Z, a-z, 0-9, -, _.')

        return super().validate(attrs)


class TokenSerializer(serializers.ModelSerializer):
    """Сериализатор токена"""

    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(max_length=200, required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя"""

    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=254)
    first_name = serializers.CharField(required=False, max_length=150)
    last_name = serializers.CharField(required=False, max_length=150)
    bio = serializers.CharField(required=False)
    role = serializers.CharField(required=False, default='user')

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        lookup_field = 'username'

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        check_user = User.objects.filter(username=username)
        check_email = User.objects.filter(email=email)

        if check_user.exists():
            raise serializers.ValidationError('Пользователь уже существует')

        if check_email.exists():
            raise serializers.ValidationError('Почта уже существует')

        request = self.context.get('request')
        id = request.auth.payload.get('user_id')
        user = get_object_or_404(User, id=id)
        role = attrs.get('role')

        roles_list = [ROLE_CHOICES[i][0] for i in range(len(ROLE_CHOICES))]

        if role is not None and role not in roles_list:
            raise ValidationError('Несуществующая роль')

        if user.is_user and 'role' in attrs and not user.is_superuser:
            attrs['role'] = 'user'

        if username is not None:
            reg = re.compile(r'^[\w.@+-]+')
            if not reg.match(username):
                raise ValidationError('Username не соответствует правилам')

        return super().validate(attrs)
