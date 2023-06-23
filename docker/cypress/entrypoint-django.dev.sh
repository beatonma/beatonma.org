#!/usr/bin/env ash

export DJANGO_SETTINGS_MODULE="basetest.frontend_test_settings"

python manage.py migrate
pytest -p no:cacheprovider

python manage.py create_test_data
python manage.py createsuperuser --noinput --username "michael" --email "michael@beatonma.org"
python manage.py runserver 0.0.0.0:8000 --noreload
