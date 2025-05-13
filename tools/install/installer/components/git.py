from .. import env
from ..shell import cmd
from .installer import Installer


class GitInstaller(Installer):
    name = "git"

    def install(self):
        cmd("git config --global credential.helper 'cache --timeout=86400'")

    def is_installed(self) -> bool:
        return env.homedir(".gitconfig").exists()
