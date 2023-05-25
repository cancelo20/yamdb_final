from django.contrib import admin

from .models import Comment, Review, Title, Category, Genre


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Админка для модели Title."""

    list_display = ('pk', 'name', 'year')
    search_fields = ('name', 'year')
    empty_value_display = '-пусто-'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Админка для модели Review."""

    list_display = (
        'pk',
        'title',
        'text',
        'author',
        'score',
        'pub_date',
    )
    search_fields = ('text', 'score', 'author')
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Админка для модели Comment."""

    list_display = (
        'pk',
        'review',
        'text',
        'author',
        'pub_date',
    )
    search_fields = ('text', 'author')
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админка для модели Category."""

    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Админка для модели Genre."""

    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'
