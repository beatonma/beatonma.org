expected_var() {
  log "expected variable '$1' is not set"
  exit 1
}

# Check expected variables
if [ ! -v FILE_ENV ]; then expected_var "FILE_ENV"; fi
if [ ! -v FILE_COMPOSE ]; then expected_var "FILE_COMPOSE"; fi
if [ ! -v BUILD_TYPE ]; then expected_var "BUILD_TYPE"; fi

source "$FILE_ENV"

# Data import/export
ARCHIVE_DIRNAME="data-archive"
ARCHIVE_DB="backup.sql"


docker_compose() {
  run_command docker compose -f "$FILE_COMPOSE" "$@"
}

docker_compose_build() {
  docker_compose build --progress=plain --ssh=default \
    --build-arg NEXT_PUBLIC_SITE_NAME="$NEXT_PUBLIC_SITE_NAME" \
    --build-arg NEXT_PUBLIC_GITHUB_USERNAME="$NEXT_PUBLIC_GITHUB_USERNAME" \
    --build-arg NEXT_PUBLIC_GOOGLE_RECAPTCHA_TOKEN="$NEXT_PUBLIC_GOOGLE_RECAPTCHA_TOKEN" \
    --build-arg NEXT_PUBLIC_GOOGLE_SITE_VERIFICATION="$NEXT_PUBLIC_GOOGLE_SITE_VERIFICATION" \
    "$@"
}


export_data() {
  docker_container_postgres="$1"

  if [ ! -v docker_container_postgres ]; then expected_var "docker_container_postgres"; fi

  local_temp_path="/tmp/$ARCHIVE_DIRNAME"
  output_filename="archive-${BUILD_TYPE}-$(date +%F).tar.gz"
  docker_temp_db_path="/tmp/$ARCHIVE_DB"

  # copy important files
  run_command mkdir -p "$local_temp_path/"
  run_command cp -r "$KEYFILES_ROOT/." "$local_temp_path/keyfiles/"
  run_command cp -r "$MEDIA_ROOT/." "$local_temp_path/media/"

  # dump database
  run_command docker exec "$docker_container_postgres" \
    pg_dump --clean --create --no-owner \
    --format=custom \
    --username="$POSTGRES_USER" \
    --file="$docker_temp_db_path" \
    "$POSTGRES_DB"
  run_command docker cp "${docker_container_postgres}:$docker_temp_db_path" "$local_temp_path"

  # build archive
  run_command tar -czvf "$output_filename" -C "/tmp" "$ARCHIVE_DIRNAME"

  # cleanup
  run_command rm -r "$local_temp_path"
  run_command docker exec "$docker_container_postgres" \
    rm "$docker_temp_db_path"
  exit 0
}


import_data() {
  docker_container_postgres="$1"
  if [ ! -v docker_container_postgres ]; then expected_var "docker_container_postgres"; fi

  archive_file="$2"
  if [ ! -v archive_file ]; then expected_var "archive_file"; fi

  local_temp_path="/tmp/$ARCHIVE_DIRNAME"
  docker_temp_db_path="/tmp/$ARCHIVE_DB"

  # extract archive
  run_command tar -xzvf "$archive_file" -C "/tmp"

  # copy important files to correct location
  run_command mkdir -p "$KEYFILES_ROOT"
  run_command cp -r "$local_temp_path/keyfiles/." "$KEYFILES_ROOT"
  run_command mkdir -p "$MEDIA_ROOT"
  run_command cp -r "$local_temp_path/media/." "$MEDIA_ROOT"

  # restore database
  run_command docker cp "$local_temp_path/$ARCHIVE_DB" "$docker_container_postgres:$docker_temp_db_path"
  run_command docker exec -i "$docker_container_postgres" \
    pg_restore --clean \
    --verbose \
    --no-owner \
    --username="$POSTGRES_USER" \
    --dbname="$POSTGRES_DB" \
    "$docker_temp_db_path"

  # cleanup
  run_command rm -r "$local_temp_path"
  run_command docker exec -i "$docker_container_postgres" rm "$docker_temp_db_path"

  exit 0
}
