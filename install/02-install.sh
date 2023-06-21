#!/usr/bin/env bash

if [ "$EUID" = 0 ]; then
  echo "This script should be used with normal user privileges."
  echo "Please run the script again without \`sudo\` "
  exit 1
fi


SELF_PATH=$(readlink -f "$0")
INSTALL_DIRNAME="$(dirname "$SELF_PATH")"
SCRIPTS_DIR="$INSTALL_DIRNAME/scripts"
PROJECT_DIR="$(dirname "$INSTALL_DIRNAME")"
export PROJECT_DIR

LOG_DIR="$PROJECT_DIR/runtime/log"
NGINX_LOG_DIR="$LOG_DIR/nginx"
export NGINX_LOG_DIR


: "
Install system requirements.
"
source "$SCRIPTS_DIR/installer_util.sh"

git config --global credential.helper 'cache --timeout=86400'
eval "$(ssh-agent -s)"
ssh-add

subscript "CHECKPOINT_BASHRC" "$SCRIPTS_DIR/setup_bashrc.sh"
subscript "CHECKPOINT_ROOTLESS_DOCKER" "$SCRIPTS_DIR/setup_rootless_docker.sh"
subscript "CHECKPOINT_CRON" "$SCRIPTS_DIR/setup_cron.sh"
subscript "CHECKPOINT_FAIL2BAN" "$SCRIPTS_DIR/setup_fail2ban.sh"
subscript "CHECKPOINT_SAMBA" "$SCRIPTS_DIR/setup_samba.sh"
subscript "_" "$SCRIPTS_DIR/check_db.sh"


: "
Install and run project.
"
run_command "cd '/home/$USERNAME/beatonma.org' || exit"
subscript "_" ./compose.sh init
subscript "_" ./compose.sh build
subscript "_" ./compose.sh up -d

log '[OK] Project configuration complete.'
log ''
log 'Your server should now be up and running!'
log ''
log 'You still need to:'
log '- Copy any previous media files to /var/www/media/.'
log '- Update static files via `gulp publish`.'
