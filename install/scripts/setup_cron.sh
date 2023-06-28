#!/usr/bin/env bash

: "
Configure system-level cron schedule for certbot certificate renewal.
"
setup_cron() {

  # minute hour dayofmonth month dayofweek
  local schedule="39 4 * * *" # 04:39 each day
  local command="$HOME/beatonma.org/bma certbot renew"

  run_command "(crontab -l ; echo '$schedule $command') | crontab -"
}

setup_cron
