#!/usr/bin/env bash


setup_rootless_docker() {
  run_command "sudo apt install -y uidmap"

  # Disable root service
  run_command "sudo systemctl disable --now docker.service docker.socket"

  # Run install script from /usr/bin
  run_command "dockerd-rootless-setuptool.sh install"

  # Run on startup
  run_command "systemctl --user enable docker"
  run_command "sudo loginctl enable-linger '$USERNAME'"

  # Allow privileged ports
  # Use `slirp4netns` so that client IP addresses can be seen by containers for logging.
  #  - see https://docs.docker.com/engine/security/rootless/#networking-errors
  override_dir=$("$HOME/.config/systemd/user/docker.service.d")
  run_command "mkdir ${override_dir}"
  run_command "echo [Service]\nEnvironment=\"DOCKERD_ROOTLESS_ROOTLESSKIT_PORT_DRIVER=slirp4netns\" > \"${override_dir}/override.conf\""
  unset override_dir
  run_command "echo 'net.ipv4.ip_unprivileged_port_start=0' >> /etc/sysctl.conf"

  run_command "sudo sysctl --system"
  run_command "systemctl --user daemon-reload"
  run_command "systemctl --user restart docker"

  log "[OK] Rootless Docker is ready to use!"
}

setup_rootless_docker
