from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorAdminModer(BasePermission):
    """Разрешение на уровне админа или пользователя."""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_superuser
            or request.user.is_admin
            or request.user.is_moderator
            or obj.author == request.user
        )


class OwnerOrAdmins(BasePermission):
    """Разрешение на уровне админа или автора."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
            obj == request.user
            or request.user.is_admin
        )


class IsAdminOrReadOnly(BasePermission):
    """Разрешение на уровне админ."""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_admin
        )


class AuthorAndStaffOrReadOnly(BasePermission):
    """Разрешение на уровне модератора или автора."""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated
            and (
                obj.author == request.user or request.user.is_moderator
            )
        )
