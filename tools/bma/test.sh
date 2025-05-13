export FILE_COMPOSE="compose.test.yml"
export FILE_ENV=".env.production"
export BUILD_TYPE="test"

usage="$(basename "$0") test
  cypress    Run cypress end-to-end tests.
"

source ./tools/bma/common.sh

run_action() {
  case "$1" in
    "-h" | "--help" | "?")
      log "$usage"
      ;;
    "cypress")
      shift
      docker_compose up cypress "$@"
      ;;
    *)
      docker_compose_build
      docker_compose up --abort-on-container-exit "$@"
      ;;
  esac
  exit 0
}
export run_action
