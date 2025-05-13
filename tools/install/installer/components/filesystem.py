import os.path

from .. import env
from ..shell import mkdir
from .installer import Installer


class FilesystemInstaller(Installer):
    name = "filesystem"

    _DIRECTORIES = [
        "/var/www",
        "/var/www/static",
        "/var/www/media",
        "/var/log/nginx",
    ]

    def install(self):
        for dir in self._DIRECTORIES:
            mkdir(dir, mode=775, owner=env.USERNAME, sudo=True)

    def is_installed(self) -> bool:
        for dir in self._DIRECTORIES:
            if not os.path.exists(dir):
                return False
        return True
