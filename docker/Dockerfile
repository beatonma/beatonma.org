ARG NODE_VERSION=22
ARG PYTHON_VERSION=3.13
ARG NGINX_VERSION=latest

################################################################################
FROM node:${NODE_VERSION}-alpine AS frontend
LABEL description="Main NextJS project."

ARG NEXT_PUBLIC_SITE_NAME
ENV NEXT_PUBLIC_SITE_NAME=$NEXT_PUBLIC_SITE_NAME

RUN apk add curl
RUN adduser -u 1001 -s /bin/sh -D app
USER app

WORKDIR /app
COPY --chown=app:app ./frontend/package.json ./frontend/package-lock.json /app/
RUN npm install

COPY --chown=app:app ./frontend /app
RUN npm run build

################################################################################
FROM python:${PYTHON_VERSION}-alpine AS python
ENV PYTHONBUFFERED 1


################################################################################
FROM python AS app_core

RUN apk add \
    curl \
    openssh-client \
    git \
    build-base


# Install private libraries from github.
RUN mkdir -p -m 0700 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts
RUN --mount=type=ssh pip install git+ssh://git@github.com/beatonma/bmanotify.git
RUN --mount=type=ssh pip install git+ssh://git@github.com/beatonma/bmanotify-django.git

COPY ./beatonma-django/requirements.txt /tmp/
RUN --mount=type=cache,target=/root/.cache/pip pip install -r /tmp/requirements.txt

ARG GIT_HASH
ENV GIT_HASH=$GIT_HASH

WORKDIR /var/log/beatonma/
WORKDIR /django

# Django project files.
COPY ./beatonma-django /django


################################################################################
FROM app_core AS app
LABEL description="Main Django project."

EXPOSE 8000

COPY "./docker/django/entrypoint.sh" /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]


################################################################################
FROM app_core AS celery
LABEL description="Celery task runner."

ENTRYPOINT ["celery", "-A", "beatonma", "worker", "-l", "info"]


################################################################################
FROM app_core AS crontab
LABEL description="Scheduled tasks."

WORKDIR /cron/
COPY ./docker/cron/cron-schedule /tmp/
COPY ./docker/cron/crontab/*.sh /cron/
RUN chmod +x /cron/*.sh
RUN crontab /tmp/cron-schedule

################################################################################
FROM nginx:${NGINX_VERSION} AS server

COPY ./docker/nginx/nginx.conf /etc/nginx/
COPY ./docker/nginx/templates/ /etc/nginx/templates/
COPY ./docker/nginx/entrypoint.sh /docker-entrypoint.d/40-letsencrypt-perms.sh
RUN chmod +x /docker-entrypoint.d/40-letsencrypt-perms.sh

EXPOSE 80
EXPOSE 443


################################################################################
FROM python AS server_checks
LABEL description="Basic tests to ensure server is up and accessible."

RUN --mount=type=cache,target=/root/.cache/pip pip install requests

COPY ./docker/config_tests/ /tmp/config_tests/
ENTRYPOINT ["python", "/tmp/config_tests/runtests.py"]
