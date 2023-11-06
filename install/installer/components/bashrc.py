import os.path

from .. import env, shell
from .installer import Installer

_BASHRC_FILENAME = ".bashrc.bma"
_BASHRC_PATH = env.homedir(_BASHRC_FILENAME)


class BashRcInstaller(Installer):
    name = "bashrc"

    def install(self):
        shell.copy_file(f"files/{_BASHRC_FILENAME}", env.HOME_DIR)
        with open(env.homedir(".bashrc"), "a") as bashrc:
            bashrc.write(f"source {_BASHRC_PATH}")

    def is_installed(self) -> bool:
        return os.path.exists(_BASHRC_PATH)
