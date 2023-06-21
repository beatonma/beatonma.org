# Environment variables
    export DOCKER_HOST=unix://$XDG_RUNTIME_DIR/docker.sock
    export DOCKER_BUILDKIT=1
    export COMPOSE_DOCKER_CLI_BUILD=1

# SSH setup
[Github guide to key generation](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)

Done that but still see `permission denied (publickey)`? Re-run `ssh-add`!


# Docker commands
For clarity, we will use the prefix `dc` below as an alias for
`docker compose -f compose.production.yml`.

## Production build
```bash
dc build --ssh default
```


## Run `pgadmin`
```bash
docker run -p 5050:80 --env-file ~/docker/pgadmin4/.env -v pgadmin:/var/lib/pgadmin --name pgadmin4 -d dpage/pgadmin4
```


# Certbot
```bash
# Initial certification.
dc run --rm certbot certonly --webroot --webroot-path /var/www/certbot/ -d inverness.io

# Renew
dc run --rm certbot renew
```


# Gotchas

- File permissions in a docker volume are inherited from their source file. Make sure shell files are executable, where applicable.
- Expose ports: https://docs.docker.com/engine/security/rootless/#exposing-privileged-ports
