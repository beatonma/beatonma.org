#!/usr/bin/env bash
if [ -d "/etc/letsencrypt/archive" ]
then
  chown -R nginx:nginx /etc/letsencrypt/archive/ /etc/letsencrypt/live/
fi

chown -R nginx:nginx /var/log/nginx/
