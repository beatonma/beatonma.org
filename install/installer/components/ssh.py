from .. import env
from ..shell import cmd
from .installer import Installer


class SshInstaller(Installer):
    name = "ssh"

    def install(self):
        cmd("eval $(ssh-agent -s)")
        cmd("ssh-add", inputs=[env.SSH_PASS])

    def is_installed(self) -> bool:
        return False
