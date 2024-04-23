location /media {
    alias /var/www/media/;
    expires 1y;
    add_header Cache-Control "public";
}

location /static {
    alias /var/www/static/;
    expires 1y;
    add_header Cache-Control "public";
}

# Server resources that are bundled alongside a webapp.
location ~ ^/webapp/.+?/.+$ {
    rewrite ^/webapp/(.+?)/(.+) /media/webapps/$1/$2 permanent;
}
