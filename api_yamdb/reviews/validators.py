from django.utils import timezone


def validate_year(year):
    now_year = timezone.now().year
    if year > now_year:
        raise ValueError(f'Некорректный год {year}')
