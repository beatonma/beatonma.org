#!/usr/bin/env ash
python manage.py migrate
python manage.py collectstatic --noinput
pytest -p no:cacheprovider

gunicorn beatonma.wsgi:application --bind 0.0.0.0:8000
