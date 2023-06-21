#!/usr/bin/env bash


setup_bashrc() {
  [ -n "$BASHRC_FILE" ] || {
    error "BASHRC_FILE $BASHRC_FILE is not set"
    exit 1
  }

  log "Updating .bashrc ($BASHRC_FILE)"
  {
    echo ''
    echo '### beatonma.org start ###'
    echo ''
    echo 'alias upd="sudo apt update && apt list --upgradeable"'
    echo 'alias upg="sudo apt upgrade"'
    echo 'alias bashrc="nano ~/.bashrc"'
    echo ''
    echo '# Enter a shell session for the specified container'
    echo 'dockershell() {'
    echo '    docker exec -it $1 sh'
    echo '}'
    echo ''
    echo '# Prepare SSH for private Github repositories.'
    echo 'sshagent() {'
    echo '    eval $(ssh-agent -s)'
    echo '    ssh-add'
    echo '}'
    echo ''
    echo '# Docker rootless'
    echo 'export DOCKER_HOST=unix://$XDG_RUNTIME_DIR/docker.sock'
    echo 'export DOCKER_BUILDKIT=1'
    echo 'export COMPOSE_DOCKER_CLI_BUILD=1'
    echo ''
  } >> "$BASHRC_FILE"

  log "[OK] Updated $BASHRC_FILE"
}

setup_bashrc
