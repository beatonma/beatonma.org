# Installation

## Ubuntu

### Create system user
```bash
# Create user, if required
adduser $username
usermod -aG sudo $username
# Login as this user before continuing
```

### Clone repository
```bash
git clone https://github.com/beatonma/beatonma.org my_directory/
```

### Install and configure
Create and populate `.env` file in `install/` directory.
```bash
cd my_directory/install
cp example.env .env && nano .env
python3 install.py  # Install docker
sudo reboot now

cd my_directory/install
python3 install.py  # Install other required system components
sudo reboot now

cd my_directory
cp example.env .env && nano .env
./bma certbot init

docker login
```

### From the user machine
```bash
ssh-copy-id username@host  # Share SSH key for passwordless ssh login and allow docker context to authenticate.
docker context create contextname --docker "host=ssh://username@host:/run/user/1000/docker.sock"
docker --context contextname ps  # Check that docker context works correctly
./bma production push

scp archive-file.tar.gz username@host:/home/username/my_directory  # Copy previous backup to server
./bma import archive-file.tar.gz
```
