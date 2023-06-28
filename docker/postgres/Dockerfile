FROM postgres:15-alpine as database

COPY ./*.db /tmp/backup.db
COPY ./restore.sh /docker-entrypoint-initdb.d/
