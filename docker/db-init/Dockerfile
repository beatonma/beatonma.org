FROM postgres:15-alpine as db_init

COPY restore.sh /
COPY backup.db /tmp/
RUN chmod +x /restore.sh

ENTRYPOINT ["/restore.sh"]
CMD ["ash"]
