################################################################################
FROM node:20-alpine AS gulp

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
COPY beatonma-gulp /app
RUN npm install && npm cache clean --force
RUN npm run build
RUN npm run jest

ENTRYPOINT ["/bin/ash"]


################################################################################
FROM python:3.11-alpine as python


################################################################################
FROM python AS app_core
LABEL maintainer="Michael Beaton <beatonma@gmail.com>"
ENV PYTHONBUFFERED 1

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

EXPOSE 8000

COPY "./docker/django/entrypoint.sh" /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]


################################################################################
FROM app_core AS celery

ENTRYPOINT ["celery", "-A", "beatonma", "worker", "-l", "info"]


################################################################################
FROM app_core as crontab

WORKDIR /cron/
COPY ./docker/cron/cron-schedule /tmp/
COPY ./docker/cron/crontab/*.sh /cron/
RUN chmox +x /cron/*.sh
RUN crontab /tmp/cron-schedule

################################################################################
FROM nginx AS server

COPY ./docker/nginx/nginx.conf /etc/nginx/
COPY ./docker/nginx/templates/ /etc/nginx/templates/
COPY ./docker/nginx/entrypoint.sh /docker-entrypoint.d/40-letsencrypt-perms.sh
RUN chmod +x /docker-entrypoint.d/40-letsencrypt-perms.sh

EXPOSE 80
EXPOSE 443


################################################################################
FROM python as server_checks

RUN --mount=type=cache,target=/root/.cache/pip pip install requests

COPY ./docker/config_tests/ /tmp/config_tests/
ENTRYPOINT ["python", "/tmp/config_tests/runtests.py"]
