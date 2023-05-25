from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r'auth', views.CodeTokenViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]
