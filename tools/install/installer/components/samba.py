import os

from .. import env
from ..shell import apt_install, cmd, copy_file, write_file
from .installer import Installer

CONFIG = """
[global]
   workgroup = WORKGROUP
   wins support = yes
   dns proxy = no
   log file = /var/log/samba/log.%m
   max log size = 1000
   syslog = 0
   panic action = /usr/share/samba/panic-action %d
   server role = standalone server
   passdb backend = tdbsam
   obey pam restrictions = yes
   unix password sync = yes
   passwd program = /usr/bin/passwd %u
   passwd chat = *Enter\snew\s*\spassword:* %n\n *Retype\snew\s*\spassword:* %n\n
   *password\supdated\ssuccessfully* .
   pam password change = yes
   map to guest = bad user
   /bin/false %u
   usershare allow guests = no
   encrypt passwords = yes
   access based share enum = yes
   public = no
   read only = no
   only guest = no
   valid users = {username}
   browseable = no
   writeable = no

[home]
   path = {home_path}
   browseable = yes
   writeable = yes
   create mask = 0644
   directory mask = 0755

[www]
  path = /var/www/
  browseable = yes
  writeable = yes
  create mask = 0644
  directory mask = 0755
"""


class SambaInstaller(Installer):
    name = "samba"

    def install(self):
        apt_install("samba")

        smb_conf = CONFIG.format(username=env.USERNAME, home_path=env.HOME_DIR)
        copy_file("/etc/samba/smb.conf", "/etc/samba/smb.conf.bak", sudo=True)
        write_file("/etc/samba/smb.conf", smb_conf, sudo=True)
        cmd(
            f"smbpasswd -as {env.USERNAME}",
            inputs=[
                env.SAMBA_PASS,
                env.SAMBA_PASS,
            ],
            sudo=True,
        )
        cmd("service smbd restart", sudo=True)

    def is_installed(self) -> bool:
        return os.path.exists("/etc/samba/smb.conf.bak")
