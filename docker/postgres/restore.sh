#!/usr/bin/env ash

BACKUP_PATH="/tmp/backup.db"

if [ ! -f "$BACKUP_PATH" ]; then
  echo "No database backup file found at '$BACKUP_PATH'."
  exit 0
fi

pg_restore --role beatonma --no-owner -d beatonma --create "$BACKUP_PATH"

# Show list of restored tables
psql -d beatonma -c "\dt"

exec "$@"
