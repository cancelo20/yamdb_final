![yamdb workflow](https://github.com/cancelo20/yamdb_final/actions/workflows/main.yml/badge.svg)

Описание

Проект YaMDb

Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles).
Произведения делятся на категории: «Книги», «Фильмы», «Музыка».
Список категорий (Category) может быть расширен администратором.

Доступен следующий функционал:

Просмотр, создание, редактирование и удаление . Просмотр и создание групп. Подписки. Возможность комментирования , редактирования и удаления комментариев.

Технологии:

Python, Django, DRF, JWT + Joser

Как запустить проект:
Установка проекта из репозитория

Клонируем проект:

git clone https://github.com/... или

git clone git@github.com:... Переходим в папку с проектом:

cd название папки Устанавливаем виртуальное окружение:

python -m venv venv Активируем виртуальное окружение:

source venv/Scripts/activate
Для деактивации виртуального окружения выполним (после работы):

deactivate Устанавливаем зависимости:

python -m pip install --upgrade pip

pip install -r requirements.txt

pip install -U djoser

pip install django-filter

Выполнить миграции:
cd api_yamdb

python manage.py makemigrations
python manage.py migrate
Запустить проект (в режиме сервера Django):
python manage.py runserver

Запуск docker-compose:
cd infra/
docker-compose up -d --build

Создание superuser:
docker-compose exec web python manage.py createsuperuser

Env-файл:
SECRET_KEY = hhz7l-ltdismtf@bzyz+rple7*s*w$jak%whj@(@u0eok^f9k4
DB_ENGINE = django.db.backends.postgresql
DB_NAME = postgres
POSTGRES_USER = postgres
POSTGRES_PASSWORD = postgres
DB_HOST = db
DB_PORT = 5432
