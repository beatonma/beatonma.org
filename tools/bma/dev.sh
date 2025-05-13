export FILE_COMPOSE="compose.dev.yml"
export FILE_ENV=".env.dev"
export BUILD_TYPE="dev"

POSTGRES_CONTAINER_NAME="dev_postgres"

usage="$(basename "$0") dev
  shell          Open a shell to run Django migrations and other commands
  export         Export database and media files to a backup archive.
  import FILE    Restore database and media files from a backup archive.
"

source ./tools/bma/common.sh

django_shell() {
  docker_compose --profile manage run --rm "$@" django_manage
}

run_action() {
  case "$1" in
    "shell")
      shift
      django_shell "$@"
      ;;
    "import")
      import_data "$POSTGRES_CONTAINER_NAME" "$2"
      ;;
    "export")
      export_data "$POSTGRES_CONTAINER_NAME"
      ;;
    *)
      log "$usage"
      ;;
  esac
  exit 0
}
export run_action
