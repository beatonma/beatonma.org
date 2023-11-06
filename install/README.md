# Installing on a new Ubuntu instance.

1. Update DNS records for server URL.

2. ```bash
   sudo apt update
   sudo apt upgrade
   sudo do-release-upgrade
   ```

3. ```bash
    git clone https://github.com/beatonma/beatonma.org beatonma.org/
    git remote rename origin github
    ```

4. [Configure SSH for private Github repositories](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)

5. Create and populate `.env` file in `install/` directory.
6Create and populate `.env` file in project directory.

6. Run `python ./install/install.py`
   > Installs `docker`.

7. Restart the system then run `python ./install/install.py` again.
   > Installs and configures the required environment for our Docker project.

8. The server should now be up and running.

9. Copy your archived `tar.gz` data to the server and restore it with `./bma import FILENAME`.
