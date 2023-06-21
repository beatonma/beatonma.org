#!/usr/bin/env bash

setup_restore_database() {
  local backup_db_path
  backup_db_path="$PROJECT_DIR/docker/db-init/backup.db"

  while [ ! -f "$backup_db_path" ]
  do
    echo "Database backup not found ($backup_db_path)"
    read -n 1 -p "Try again?"
  done
}

setup_restore_database
