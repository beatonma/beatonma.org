export FILE_COMPOSE="compose.production.yml"
export FILE_ENV=".env.production"
export BUILD_TYPE="production"

POSTGRES_CONTAINER_NAME="postgres"

usage="$(basename "$0") production
  shell            Open a shell in the running Django container.
  export           Export database and media files to a backup archive.
  import FILE      Restore database and media files from a backup archive.
  certbot init     Configure certbot in a new installation.
  certbot renew    Update certbot certificates.
"

source ./tools/bma/common.sh

docker_push() {
  run_command docker push fallofmath/beatonma:crontab
  run_command docker push fallofmath/beatonma:django
  run_command docker push fallofmath/beatonma:celery
  run_command docker push fallofmath/beatonma:next
  run_command docker push fallofmath/beatonma:nginx
  run_command docker push fallofmath/beatonma:startup_checks
  run_command docker --context "$DOCKER_REMOTE_CONTEXT" compose -f compose.production.yml pull
  run_command docker --context "$DOCKER_REMOTE_CONTEXT" compose -f compose.production.yml down
  run_command docker --context "$DOCKER_REMOTE_CONTEXT" compose -f compose.production.yml up -d
}

django_shell() {
  run_command docker exec -it django sh
  exit 0
}


certbot_init() {
  # Run this before first run of production server.
  run_command docker run --rm \
    --name certbot_init \
    --volume letsencrypt_keys:/etc/letsencrypt:rw \
    --volume letsencrypt_webroot:/var/www/letsencrypt:rw \
    --env-file "$FILE_ENV" \
    --entrypoint "" \
    -p 80:80 \
    certbot/certbot:latest \
    sh -c "certbot certonly --standalone $*"
}

certbot_renew() {
  # Run this periodically to update while production server is running.
  run_command docker run --rm \
    --name certbot_renew \
    --volume letsencrypt_keys:/etc/letsencrypt:rw \
    --volume letsencrypt_webroot:/var/www/letsencrypt:rw \
    --env-file "$FILE_ENV" \
    --entrypoint "" \
    certbot/certbot:latest \
    sh -c "certbot certonly --webroot -w /var/www/letsencrypt $*"
    run_command docker container restart nginx
}

certbot() {
  common_args_list=(
    "-d ${DOMAIN_NAME}"
    "-d www.${DOMAIN_NAME}"
    "--email ${DOMAIN_EMAIL}"
    "--rsa-key-size 4096"
    "--keep-until-expiring"
    "--agree-tos"
    "--non-interactive"
  )

  # Concat list to string
  common_args=$(printf "%s " "${common_args_list[@]}")

  case "$1" in
    "init")
      shift
      certbot_init "$common_args"
      ;;
    "renew")
      shift
      certbot_renew "$common_args"
      ;;
    *)
      log "Unknown certbot command '$1'"
  esac

  exit 0
}


run_action() {
  case "$1" in
    "certbot")
      shift
      certbot "$@"
      ;;
    "shell")
      django_shell
      ;;
    "push")
      docker_compose_build
      docker_push
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
