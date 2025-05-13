#!/usr/bin/env ash

python manage.py migrate
python manage.py collectstatic --noinput
pytest -p no:cacheprovider || exit $?

python manage.py create_sample_data
python manage.py sample_github_data

python manage.py createsuperuser --noinput --username "michael" --email "michael@beatonma.org"

python manage.py runserver_plus 0.0.0.0:8000
