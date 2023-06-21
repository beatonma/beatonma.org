#!/usr/bin/env bash

setup_fail2ban() {
  apt_install fail2ban

  local fail2ban_conf_file
  fail2ban_conf_file=$(rootpath "/etc/fail2ban/jail.local")

  local fail2ban_4xx_filter_file
  fail2ban_4xx_filter_file=$(rootpath "/etc/fail2ban/filter.d/nginx-4xx.conf")

  (
    echo "[DEFAULT]"
    echo "bantime.incremement = true"
    echo "bantime.maxtime = 48h"
    echo "bantime.multipliers = 1 2 5 10 15 30 60 300 720 1440"
    echo "bantime = 1m"
    echo "findtime = 1m"
    echo "maxretry = 5"
    echo ""
    echo "[sshd]"
    echo "enabled = true"
    echo "port    = ssh"
    echo "logpath = %(sshd_log)s"
    echo "backend = %(sshd_backend)s"
    echo ""
    echo "[nginx-http-auth]"
    echo "enabled = true"
    echo "port = http, https"
    echo "logpath = ${NGINX_LOG_DIR}/error.log"
    echo ""
    echo "[nginx-all]"
    echo "enabled = true"
    echo "port = http,https"
    echo "logpath = ${NGINX_LOG_DIR}/access.log"
    echo "findtime = 60"
    echo "maxretry = 300"
    echo ""
    echo "[nginx-4xx]"
    echo "enabled = true"
    echo "port = http,https"
    echo "logpath = ${NGINX_LOG_DIR}/access.log"
    echo "findtime = 30"
    echo "maxretry = 20"
    echo ""
  ) | run_command "sudo tee $fail2ban_conf_file"

  # Based on https://gist.github.com/AysadKozanoglu/1335735272fb3b00a03bd3eea22af818
  (
    echo "[Definition]"
    echo 'failregex = ^<HOST>.*"(GET|POST).*" (404|444|403|400) .*$'
    echo "ignoreregex = "
  ) | run_command "sudo tee $fail2ban_4xx_filter_file"

  run_command "sudo systemctl enable fail2ban"
  run_command "sudo systemctl start fail2ban"

  log "[OK] Installed and configured fail2ban."
}

setup_fail2ban
