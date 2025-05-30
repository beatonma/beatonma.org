import os.path

from .. import env
from ..shell import cmd, mkdir
from .installer import Installer


class FilesystemInstaller(Installer):
    name = "filesystem"

    _DIRECTORIES = [
        "/var/log/nginx",
        "/var/www/media",
        "/var/www/static",
    ]

    def install(self):
        for _dir in self._DIRECTORIES:
            mkdir(_dir, mode=775, owner=env.USERNAME, sudo=True)

        # This group will be mapped to group 19283 inside the docker containers.
        # (by default, according to contents of /etc/subgid on the host)
        # Any user that needs to write to /var/www/media must be in that group.
        cmd("groupadd -g 119282 docker_bma", sudo=True)
        cmd("chown -R :docker_bma /var/www/media", sudo=True)

    def is_installed(self) -> bool:
        for _dir in self._DIRECTORIES:
            if not os.path.exists(_dir):
                return False
        return True
