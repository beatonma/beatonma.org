from .. import env
from ..shell import cmd
from .installer import Installer


class CronInstaller(Installer):
    name = "cron"

    def install(self):
        schedule = "39 4 * * *"  # 04:39 each day
        command = f"{env.homedir('beatonma.org/bma certbot renew')}"

        cmd(f"echo '{schedule} {command}' | crontab -")

    def is_installed(self) -> bool:
        return (
            cmd("crontab -l", throw=False).code == 0
            and cmd("crontab -l | grep 'certbot renew'").code == 0
        )
