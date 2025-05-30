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
WORKDIR /app
COPY ./frontend/package.json ./frontend/package-lock.json /app/
RUN npm ci && npm cache clean --force

COPY ./frontend /app

ARG NEXT_PUBLIC_SITE_NAME
ENV NEXT_PUBLIC_SITE_NAME=$NEXT_PUBLIC_SITE_NAME

ARG NEXT_PUBLIC_SITE_BASE_URL
ENV NEXT_PUBLIC_SITE_BASE_URL=$NEXT_PUBLIC_SITE_BASE_URL


###
FROM python AS builder_django

RUN apk add --no-cache \
    openssh-client \
    git \
    build-base

RUN --mount=type=ssh \
    --mount=type=cache,target=/root/.cache/pip,id=pipcache \
    mkdir -p -m 0700 ~/.ssh \
    && ssh-keyscan github.com >> ~/.ssh/known_hosts \
    && pip install git+ssh://git@github.com/beatonma/bmanotify.git \
                   git+ssh://git@github.com/beatonma/bmanotify-django.git

COPY ./beatonma-django/requirements.txt /tmp/
RUN --mount=type=cache,target=/root/.cache/pip,id=pipcache pip install -r /tmp/requirements.txt

###
FROM python AS core_django

RUN apk add --no-cache \
    curl \
    libwebp

ARG PYTHON_VERSION
COPY --from=builder_django /usr/local/lib/python${PYTHON_VERSION}/site-packages /usr/local/lib/python${PYTHON_VERSION}/site-packages

RUN addgroup -g 19283 docker_bma \
    && mkdir -p /var/log/beatonma/ \
    && chown :docker_bma /var/log/beatonma/ \
    && chmod 2775 /var/log/beatonma/
WORKDIR /django

EXPOSE 8000


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
FROM core_nextjs AS builder_production_nextjs
RUN npm run build

###
FROM node:${NODE_VERSION}-alpine AS production_nextjs

RUN apk add curl --no-cache
RUN addgroup -S app && adduser -S app -G app
USER app
WORKDIR /app

COPY --from=builder_production_nextjs --chown=app:app /app/.next/standalone ./
COPY --from=builder_production_nextjs --chown=app:app /app/package.json ./

ENV HOSTNAME="0.0.0.0"
ENV PORT="3000"
EXPOSE 3000
ENTRYPOINT ["node", "server.js"]


###
FROM core_django AS production_core_django
COPY ./beatonma-django /django


###
FROM production_core_django AS production_django

COPY ./tools/docker/django/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh && adduser -S django -G docker_bma
USER django

ENTRYPOINT ["/entrypoint.sh"]


###
FROM production_core_django AS production_celery

RUN adduser -S celery -G docker_bma
USER celery

ENTRYPOINT ["python", "-m", "celery", "-A", "beatonma", "worker", "-l", "info"]


###
FROM core_nginx AS production_nginx

COPY ./tools/docker/nginx/nginx.conf /etc/nginx/
COPY ./tools/docker/nginx/templates/ /etc/nginx/templates/
COPY ./tools/docker/nginx/entrypoint.sh /docker-entrypoint.d/40-letsencrypt-perms.sh
RUN chmod +x /docker-entrypoint.d/40-letsencrypt-perms.sh

COPY --from=builder_production_nextjs --chown=nginx:nginx /app/.next/static /var/www/static-nextjs
COPY --from=builder_production_nextjs --chown=nginx:nginx /app/public /var/www/public-nextjs


###
FROM python AS production_server_checks

RUN --mount=type=cache,target=/root/.cache/pip,id=pipcache pip install requests
COPY ./tools/docker/config_tests/ /tmp/config_tests/
RUN adduser -S startup
USER startup
ENTRYPOINT ["python", "/tmp/config_tests/runtests.py"]


###
FROM production_core_django AS production_crontab

RUN adduser -S cronuser -G docker_bma
WORKDIR /cron/
COPY ./tools/docker/cron/cron-schedule /tmp/
COPY --chown=cronuser --chmod=+x ./tools/docker/cron/crontab/*.sh /cron/
RUN crontab -u cronuser /tmp/cron-schedule
ENTRYPOINT ["crond", "-f"]


###################
#                 #
#   Development   #
#                 #
###################

###
FROM core_nextjs AS dev_nextjs
RUN apk add curl --no-cache
ENTRYPOINT ["npm", "run", "dev"]


###
FROM core_django AS dev_django
COPY ./tools/docker/django/entrypoint.dev.sh /
ENTRYPOINT ["/entrypoint.dev.sh"]

###
FROM core_django AS dev_celery
ENTRYPOINT ["python", "-m", "celery", "-A", "beatonma", "worker", "-l", "info"]


###
FROM core_nginx AS dev_nginx
COPY ./tools/docker/nginx/templates/ /etc/nginx/templates/
COPY ./tools/docker/nginx/nginx.dev.conf /etc/nginx/nginx.conf


#####################
#                   #
#   Cypress Tests   #
#                   #
#####################

###
FROM core_django AS test_django
COPY ./tools/docker/cypress/entrypoint-django.dev.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]


###
FROM production_nextjs AS test_nextjs


###
FROM cypress/included AS test_cypress

ARG NEXT_PUBLIC_SITE_NAME
ENV NEXT_PUBLIC_SITE_NAME=$NEXT_PUBLIC_SITE_NAME

ARG NEXT_PUBLIC_SITE_BASE_URL
ENV NEXT_PUBLIC_SITE_BASE_URL=$NEXT_PUBLIC_SITE_BASE_URL

ARG NEXT_PUBLIC_GITHUB_USERNAME
ENV NEXT_PUBLIC_GITHUB_USERNAME=$NEXT_PUBLIC_GITHUB_USERNAME

WORKDIR /cypress
EXPOSE 8000
