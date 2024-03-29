from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    CategoriesViewSet,
    CommentViewSet,
    GenresViewSet,
    ReviewViewSet,
    TitlesViewSet
)


v1_router = DefaultRouter()
v1_router.register('titles', TitlesViewSet)
v1_router.register('genres', GenresViewSet, basename='genres')
v1_router.register('categories', CategoriesViewSet, basename='categories')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='review'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment',
)


urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
