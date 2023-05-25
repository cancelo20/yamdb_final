import uuid

from django.shortcuts import get_object_or_404
from django.core.mail import send_mail

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

from .models import User
from .serializers import (
    RegistrationSerializer,
    TokenSerializer,
    UserSerializer,
)
from .permissions import IsAdmin


class CodeTokenViewSet(ModelViewSet):
    """Класс аутентификации пользователя."""

    queryset = User.objects.all()
    serializer_class = RegistrationSerializer

    @action(detail=False, methods=['post'], url_path='signup')
    def code_generation(self, request):
        """Генерация confirmation_code по данным email и username."""

        username = request.data.get('username')
        email = request.data.get('email')
        confirmation_code = str(uuid.uuid4())
        serializer = self.get_serializer(data=request.data)

        if not User.objects.filter(username=username, email=email).exists():
            serializer.is_valid(raise_exception=True)
            User.objects.create(
                username=username,
                email=email,
                confirmation_code=confirmation_code,
            )
            send_mail(
                'Регистрация',
                message=f'Код подтверждения: {confirmation_code}',
                from_email='admin@yambd.ru',
                recipient_list=[email],
            )
            return Response(request.data, status=status.HTTP_200_OK)

        User.objects.update(confirmation_code=confirmation_code)
        send_mail(
            'Регистрация',
            message=f'Ваш код подтверждения: {confirmation_code}',
            from_email='admin@yambd.ru',
            recipient_list=[email],
        )
        return Response(request.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['post'],
        url_path='token',
        serializer_class=TokenSerializer,
    )
    def token_generation(self, request):
        """Генерация JWT-токена по данным confirmation_code и username."""

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = request.data.get('confirmation_code')
        username = get_object_or_404(
            User, username=request.data.get('username')
        )

        try:
            user = User.objects.get(
                username=username, confirmation_code=confirmation_code
            )
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user=user)
        return Response({'token': str(refresh.access_token)})


class UserViewSet(ModelViewSet):
    """Класс управления информацией о пользователях."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdmin,)
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ('post', 'get', 'patch', 'delete')

    @action(
        detail=False,
        methods=['get'],
        url_path='me',
        permission_classes=(IsAuthenticated,))
    def get_self_user_info(self, request):
        """Получение информациеи пользователя о самом себе."""

        user = get_object_or_404(User, username=self.request.user)
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @get_self_user_info.mapping.patch
    def update_self_user_info(self, request):
        """Изменение информации пользователя о самом себе"""

        user = get_object_or_404(User, username=self.request.user)
        serializer = self.get_serializer(
            user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
