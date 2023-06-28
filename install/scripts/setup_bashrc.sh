#!/usr/bin/env bash


HOME_DIR="/home/$USERNAME"
SCRIPT_FILE=$(rootpath "$HOME_DIR/.bashrc.bma")

setup_bashrc() {
  log "Updating .bashrc"
  {
    echo 'alias upd="sudo apt update && apt list --upgradeable"'
    echo 'alias upg="sudo apt upgrade"'
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
  } >> "$SCRIPT_FILE"

  {
    echo "source $SCRIPT_FILE"
    echo ''
  } >> "$(rootpath "$HOME_DIR/.bashrc")"

  log "[OK] Updated .bashrc"
}

setup_bashrc
