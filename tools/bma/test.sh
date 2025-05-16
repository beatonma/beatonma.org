export FILE_COMPOSE="compose.test.yml"
export FILE_ENV=".env.dev"
export BUILD_TYPE="test"

usage="$(basename "$0") test
  cypress | e2e    Run cypress end-to-end tests.
  unit             Run all unit tests from django and next.js.
"

source ./tools/bma/common.sh

unittests() {
  docker_compose run --rm --entrypoint=pytest --env DJANGO_SETTINGS_MODULE="basetest.frontend_test_settings" --no-TTY django &
  docker_compose run --rm --entrypoint="npm run jest" next &
  wait
}

run_action() {
  case "$1" in
    "-h" | "--help" | "?")
      log "$usage"
      ;;
    "unit")
      unittests
      ;;
    "cypress" | "e2e")
      shift
      docker_compose up cypress "$@"
      ;;
    *)
      unittests
      docker_compose_build
      docker_compose up --abort-on-container-exit "$@"
      ;;
  esac
  exit 0
}
export run_action
