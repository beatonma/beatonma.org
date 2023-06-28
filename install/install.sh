#!/usr/bin/env bash

if [ "$EUID" = 0 ]; then
  echo "This script should be used with normal user privileges."
  echo "Please run the script again without \`sudo\` "
  exit 1
fi


# Make sure docker is installed first.
if ! command -v docker &> /dev/null; then
  bash ./scripts/install-docker.sh
  echo "Please restart the system then run 'install.sh' again."
  exit 0
fi


SELF_PATH=$(readlink -f "$0")
INSTALL_DIRNAME="$(dirname "$SELF_PATH")"
SCRIPTS_DIR="$INSTALL_DIRNAME/scripts"
PROJECT_DIR="$(dirname "$INSTALL_DIRNAME")"

export PROJECT_DIR
export NGINX_LOG_DIR="/var/log/nginx"
export USERNAME="ubuntu"


: "
Install system requirements.
"
source "$SCRIPTS_DIR/installer_util.sh"

: "
Create required directories.
"
run_command "sudo mkdir /var/www/ || true"
run_command "sudo chown '$USERNAME':'$USERNAME' $(rootpath "/var/www/")"
run_command "mkdir $(rootpath "/var/www/static/") || true"
run_command "mkdir $(rootpath "/var/www/media/") || true"
run_command "sudo mkdir $(rootpath "$NGINX_LOG_DIR") || true"
run_command "sudo chown -R $USERNAME:$USERNAME $(rootpath "$NGINX_LOG_DIR")"


git config --global credential.helper 'cache --timeout=86400'
eval "$(ssh-agent -s)"
ssh-add

subscript "$SCRIPTS_DIR/setup_bashrc.sh"
subscript "$SCRIPTS_DIR/setup_rootless_docker.sh"
subscript "$SCRIPTS_DIR/setup_cron.sh"
subscript "$SCRIPTS_DIR/setup_fail2ban.sh"
subscript "$SCRIPTS_DIR/setup_samba.sh"

: "
Make sure database backup file is in place.
"
subscript "$SCRIPTS_DIR/check_db.sh"

: "
Install and run project.
"
run_command "cd '/home/$USERNAME/beatonma.org' || exit"
subscript ./bma certbot init
subscript ./bma production build
subscript ./bma production up -d

log '[OK] Project configuration complete.'
log ''
log 'Your server should now be up and running!'
log ''
log 'You still need to:'
log '- Copy any previous media files to /var/www/media/.'
log '- Update static files via `gulp publish`.'
