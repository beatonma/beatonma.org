import os

from beatonma.settings import environment

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": environment.POSTGRES_DB,
        "USER": environment.POSTGRES_USER,
        "PASSWORD": environment.POSTGRES_PASSWORD,
        "HOST": environment.POSTGRES_HOST,
        "PORT": environment.POSTGRES_PORT,
    }
}
