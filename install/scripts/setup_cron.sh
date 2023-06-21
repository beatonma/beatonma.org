#!/usr/bin/env bash

: "
Configure system-level cron schedule for certbot certificate renewal.
"
setup_cron() {
  local command=""
  local schedule=""

  command="/home/$USERNAME/beatonma.org/compose.sh certbot"

  # minute hour dayofmonth month dayofweek
  schedule="39 4 5,19 * *" # 4:39 on the 5th and 19th of every month

  run_command "(crontab -l ; echo '$schedule $command') | crontab -"
}

setup_cron
