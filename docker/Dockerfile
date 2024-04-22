ARG NODE_VERSION=21
ARG PYTHON_VERSION=3.12
ARG NGINX_VERSION=latest

################################################################################
FROM node:${NODE_VERSION}-alpine AS gulp
LABEL description="Generate frontend webapp and template files."

ARG GIT_HASH
ARG WEBMAIL_CONTACT_EMAIL
ARG GOOGLE_RECAPTCHA_TOKEN
ARG SITE_NAME

ENV GIT_HASH=$GIT_HASH
ENV WEBMAIL_CONTACT_EMAIL=$WEBMAIL_CONTACT_EMAIL
ENV GOOGLE_RECAPTCHA_TOKEN=$GOOGLE_RECAPTCHA_TOKEN
ENV SITE_NAME=$SITE_NAME

WORKDIR /app
COPY beatonma-gulp/package.json /app
RUN npm install && npm cache clean --force

COPY beatonma-gulp /app
RUN npm run build
RUN npm run jest

ENTRYPOINT ["/bin/ash"]


################################################################################
FROM python:${PYTHON_VERSION}-alpine as python
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

# Generated template and static files from gulp build.
COPY --from=gulp /app/dist /django


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
FROM app_core as crontab
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
FROM python as server_checks
LABEL description="Basic tests to ensure server is up and accessible."

RUN --mount=type=cache,target=/root/.cache/pip pip install requests

COPY ./docker/config_tests/ /tmp/config_tests/
ENTRYPOINT ["python", "/tmp/config_tests/runtests.py"]
