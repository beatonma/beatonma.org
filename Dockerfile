ARG NODE_VERSION=22
ARG PYTHON_VERSION=3.13
ARG NGINX_VERSION=latest

##########################
#                        #
#   Common base stages   #
#                        #
##########################

###
FROM python:${PYTHON_VERSION}-alpine AS python
ENV PYTHONBUFFERED 1

###
FROM node:${NODE_VERSION}-alpine AS core_nextjs

RUN apk add curl
RUN adduser -u 1001 -s /bin/sh -D app
USER app

WORKDIR /app
COPY --chown=app:app ./frontend/package.json ./frontend/package-lock.json /app/
RUN npm install

COPY --chown=app:app ./frontend /app


###
FROM python AS core_django

RUN apk add \
    curl \
    openssh-client \
    git \
    build-base \
    libwebp

# Install private libraries from github.
RUN mkdir -p -m 0700 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts
RUN --mount=type=ssh pip install git+ssh://git@github.com/beatonma/bmanotify.git
RUN --mount=type=ssh pip install git+ssh://git@github.com/beatonma/bmanotify-django.git

WORKDIR /var/log/beatonma/
WORKDIR /django

COPY ./beatonma-django/requirements.txt /django/
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt


###
FROM nginx:${NGINX_VERSION} AS core_nginx

EXPOSE 80
EXPOSE 443


##################
#                #
#   Production   #
#                #
##################

###
FROM core_nextjs AS production_nextjs

ARG NEXT_PUBLIC_SITE_NAME
ENV NEXT_PUBLIC_SITE_NAME=$NEXT_PUBLIC_SITE_NAME

RUN npm run build
ENTRYPOINT ["npm", "run", "start"]

###
FROM core_django AS production_core_django

COPY ./beatonma-django /django


###
FROM production_core_django AS production_django

EXPOSE 8000
COPY "./docker/django/entrypoint.sh" /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]


###
FROM production_core_django AS production_celery

ENTRYPOINT ["celery", "-A", "beatonma", "worker", "-l", "info"]


###
FROM core_nginx AS production_nginx

COPY ./docker/nginx/nginx.conf /etc/nginx/
COPY ./docker/nginx/templates/ /etc/nginx/templates/
COPY ./docker/nginx/entrypoint.sh /docker-entrypoint.d/40-letsencrypt-perms.sh
RUN chmod +x /docker-entrypoint.d/40-letsencrypt-perms.sh


###
FROM python AS production_server_checks

RUN --mount=type=cache,target=/root/.cache/pip pip install requests

COPY ./docker/config_tests/ /tmp/config_tests/
ENTRYPOINT ["python", "/tmp/config_tests/runtests.py"]


###
FROM production_core_django AS production_crontab

WORKDIR /cron/
COPY ./docker/cron/cron-schedule /tmp/
COPY ./docker/cron/crontab/*.sh /cron/
RUN chmod +x /cron/*.sh
RUN crontab /tmp/cron-schedule
ENTRYPOINT ["crond", "-f"]


###################
#                 #
#   Development   #
#                 #
###################

###
FROM core_nextjs AS dev_nextjs
ENTRYPOINT ["npm", "run", "dev"]


###
FROM core_django AS dev_django

COPY ./docker/django/entrypoint.dev.sh /

EXPOSE 8000
ENTRYPOINT ["/entrypoint.dev.sh"]

################################################################################
FROM core_django AS dev_celery

ENTRYPOINT ["celery", "-A", "beatonma", "worker", "-l", "info"]


###
FROM core_nginx AS dev_nginx

COPY ./docker/nginx/templates/ /etc/nginx/templates/
COPY ./docker/nginx/nginx.dev.conf /etc/nginx/nginx.conf


#####################
#                   #
#   Cypress Tests   #
#                   #
#####################

###
FROM core_django AS test_django
COPY ./docker/cypress/entrypoint-django.dev.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]


###
FROM cypress/included AS test_cypress

WORKDIR /cypress
COPY ./docker/cypress/entrypoint-cypress.dev.sh /entrypoint.sh

EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]
