from ..shell import append_file, chmod, cmd
from .installer import Installer

SWAPFILE = "/swapfile"


class SwapfileInstaller(Installer):
    name = "swapfile"

    def install(self):
        cmd(f"fallocate -l 1G {SWAPFILE}", sudo=True)
        chmod(600, SWAPFILE, sudo=True)
        cmd(f"mkswap {SWAPFILE}", sudo=True)
        cmd(f"swapon {SWAPFILE}", sudo=True)
        append_file("/etc/fstab", f"{SWAPFILE} swap swap defaults 0 0", sudo=True)

    def is_installed(self) -> bool:
        result = cmd("swapon --show")
        return SWAPFILE in result.output
