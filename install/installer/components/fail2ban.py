import os

from ..shell import apt_install, cmd, copy_file
from .installer import Installer


class Fail2BanInstaller(Installer):
    name = "fail2ban"

    def install(self):
        apt_install("fail2ban")
        copy_file("files/fail2ban/*", "/etc/fail2ban/", sudo=True)

    def is_installed(self) -> bool:
        return os.path.exists("/etc/fail2ban/jail.local")
