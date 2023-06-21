#!/usr/bin/env ash

pg_restore --role beatonma --no-owner -d beatonma --create /tmp/backup.db

# Show list of restored tables
psql -d beatonma -c "\dt"

exec "$@"
