#!/usr/bin/env ash
python manage.py migrate
python manage.py collectstatic --noinput
python -m pytest -p no:cacheprovider || exit $?

python manage.py createsuperuser --noinput

python -m gunicorn beatonma.wsgi:application --bind 0.0.0.0:8000
