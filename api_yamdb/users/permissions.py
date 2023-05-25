from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Проверка, что пользователь админ или суперюзер."""

    def has_permission(self, request, view):
        return request.user and (
            request.user.is_authenticated
            and request.user.is_admin
        )


class IsModer(BasePermission):
    """Проверка, что пользователь модератор."""

    def has_permission(self, request, view):
        return request.user and (
            request.user.is_authenticated
            and request.user.is_moder
        )
