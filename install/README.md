# Installing on a new Ubuntu instance.

1. ```bash
   sudo apt update
   sudo apt upgrade
   sudo do-release-upgrade
   ```

2. ```bash
    git clone https://github.com/beatonma/beatonmadotorg-django beatonma.org/
    git remote rename origin github
    ```
3. [Configure SSH for private Github repositories](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)

4. Create and populate `.env` file in project directory.

5. Update DNS records for target URL.

6. Run `bash ./install/01-install-docker.sh`

7. Restart the system then run `bash ./install/02-install.sh`
    - Creates `/var/www/` asset directories.
    - Installs and configures `samba`.
    - Adds useful commands to `~/.bashrc`.
    - Configures rootless docker.
    - Initialises certbot certificates.
    - Initialises database volume from backup.
    - Creates `cron` schedule to update certbot certificates periodically.
    - Configures fail2ban.
    - Builds and runs the server.
