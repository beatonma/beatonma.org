# Installing on a new Ubuntu instance.

1. ```bash
   sudo apt update
   sudo apt upgrade
   sudo do-release-upgrade
   ```

2. ```bash
    git clone https://github.com/beatonma/beatonma.org beatonma.org/
    git remote rename origin github
    git submodule init
    ```

3. [Configure SSH for private Github repositories](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)

4. Create and populate `.env` file in `install/` directory.
5. Create and populate `.env` file in project directory.

6. Run `python3 install.py`
   > Installs `docker`.

7. Restart the system then run `python3 install.py` again.
   > Installs and configures the required environment for our Docker project.
   
8. Update DNS records and ensure ports 80 and 443 are open.

9. Initialize `certbot`:  
   ```bash
   ./bma certbot init
   ```

10. Build server images:  
   ```bash
   eval $(ssh-agent -s) && ssh-add
   ./bma pull
   ./bma production build
   ```

11. Start the server:  
   ```bash
   ./bma production up -d
   ```

12. Copy your archived `tar.gz` data to the server and restore it:  
   ```./bma import FILENAME.```
