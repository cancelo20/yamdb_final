from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from users.models import User
from .validators import validate_year

STR_MAX_LENGTH = 15


class TitleImport(models.Model):
    """Модель для csv-файла."""

    cvs_file = models.FileField(upload_to='static/data/')
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date_added',)


class Genre(models.Model):
    """Модель жанра."""

    name = models.CharField('Имя жанра', max_length=256)
    slug = models.SlugField('Слаг жанра', max_length=50, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.slug


class Category(models.Model):
    """Модель категорий."""

    name = models.CharField('Имя категории', max_length=256)
    slug = models.SlugField('Слаг категории', max_length=50, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.slug


class Title(models.Model):
    """Модель заголовка."""

    name = models.CharField('Наименование', max_length=150)
    year = models.PositiveSmallIntegerField(
        'Год релиза',
        validators=(validate_year,),
        help_text='Введите год релиза',
    )
    genre = models.ManyToManyField(
        Genre, verbose_name='Жанр', related_name='title', through='GenreTitle'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        help_text='Введите категорию произведения',
        null=True,
        blank=True,
        related_name='titles',
    )
    description = models.TextField('Описание', null=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:STR_MAX_LENGTH]


class GenreTitle(models.Model):
    """Вспомогающая модель для жанра/заголовка."""

    genre = models.ForeignKey(
        Genre, verbose_name='Жанр', on_delete=models.CASCADE
    )
    title = models.ForeignKey(
        Title, verbose_name='Заголовок', on_delete=models.CASCADE
    )

    class Meta:
        ordering = ('genre',)
        verbose_name = 'Заголовок для жанра'
        verbose_name_plural = 'Заголовки для жанров'

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    """Модель отзыва"""

    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    title = models.ForeignKey(
        Title,
        verbose_name='Заголовок',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.TextField('Отзыв')
    score = models.IntegerField(
        'Рейтинг',
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        unique_together = ('author', 'title')

    def __str__(self):
        return self.text[:STR_MAX_LENGTH]


class Comment(models.Model):
    """Модель комментариев."""

    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    review = models.ForeignKey(
        Review,
        verbose_name='Заголовок',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField('Заголовок')
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:STR_MAX_LENGTH]
