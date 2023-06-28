# Installing on a new Ubuntu instance.

1. ```bash
   sudo apt update
   sudo apt upgrade
   sudo do-release-upgrade
   ```

2. ```bash
    git clone https://github.com/beatonma/beatonma.org beatonma.org/
    git remote rename origin github
    ```
3. [Configure SSH for private Github repositories](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)

4. Create and populate `.env` file in project directory.

5. Update DNS records for target URL.

6. Run `bash ./install/install.sh`

7. Restart the system then run `bash ./install/install.sh` again.

8. Once done, the server should be up and running!
