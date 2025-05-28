import os.path

from .. import env
from ..shell import mkdir
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

    def is_installed(self) -> bool:
        for _dir in self._DIRECTORIES:
            if not os.path.exists(_dir):
                return False
        return True
