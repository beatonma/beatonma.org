#!/usr/bin/env bash


setup_samba() {
  :"
  Create asset directories.
  "
  run_command "sudo mkdir /var/www/ || true"
  run_command "sudo chown '$USERNAME':'$USERNAME' $(rootpath "/var/www/")"
  run_command "mkdir $(rootpath "/var/www/static/") || true"
  run_command "mkdir $(rootpath "/var/www/media/") || true"

  : "
  Configure samba.
  "
  local samba_conf_file
  samba_conf_file=$(rootpath "/etc/samba/smb.conf")

  log "Installing samba..."
  apt_install samba
  {
    echo '[global]'
    echo '   workgroup = WORKGROUP'
    echo '   wins support = yes'
    echo '   dns proxy = no'
    echo '   log file = /var/log/samba/log.%m'
    echo '   max log size = 1000'
    echo '   syslog = 0'
    echo '   panic action = /usr/share/samba/panic-action %d'
    echo '   server role = standalone server'
    echo '   passdb backend = tdbsam'
    echo '   obey pam restrictions = yes'
    echo '   unix password sync = yes'
    echo '   passwd program = /usr/bin/passwd %u'
    echo '   passwd chat = *Enter\snew\s*\spassword:* %n\n *Retype\snew\s*\spassword:* %n\n'
    echo '   *password\supdated\ssuccessfully* .'
    echo '   pam password change = yes'
    echo '   map to guest = bad user'
    echo '   /bin/false %u'
    echo '   usershare allow guests = no'
    echo '   encrypt passwords = yes'
    echo '   access based share enum = yes'
    echo '   public=no'
    echo '   read only=no'
    echo '   only guest=no'
    echo "   valid users=$USERNAME"
    echo '   browseable=no'
    echo '   writeable=no'
    echo ''
    echo '[home]'
    echo '   path=/home/ubuntu'
    echo '   browseable=yes'
    echo '   writeable=yes'
    echo '   create mask=0644'
    echo '   directory mask=0755'
    echo ''
    echo '[www]'
    echo '  path=/var/www/'
    echo '  browseable=yes'
    echo '  writeable=yes'
    echo '  create mask=0644'
    echo '  directory mask=0755'
  } | run_command "sudo tee $samba_conf_file"
  run_command "sudo smbpasswd -a $USERNAME"
  run_command "sudo service smbd restart"
  log "[OK] Installed and configured samba."
}

setup_samba
