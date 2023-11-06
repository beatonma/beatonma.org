import os

from .. import env
from ..shell import apt_install, apt_update, cmd, copy_file, is_installed, mkdir
from .installer import Installer


class DockerInstaller(Installer):
    name = "docker"

    def install(self):
        # Prerequisites
        apt_install("ca-certificates", "curl", "gnupg", "lsb-release")

        # Add Docker GPG key
        mkdir("/etc/apt/keyrings")
        cmd(
            "curl -fsSL https://download.docker.com/linux/ubuntu/gpg | "
            "sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg"
        )
        # Add Docker repository
        cmd(
            "echo "
            '"deb [arch=$(dpkg --print-architecture) '
            "signed-by=/etc/apt/keyrings/docker.gpg] "
            'https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" '
            "| sudo tee /etc/apt/sources.list.d/docker.list > /dev/null"
        )
        apt_update()
        apt_install(
            "docker-ce", "docker-ce-cli", "containerd.io", "docker-compose-plugin"
        )

    def is_installed(self) -> bool:
        return is_installed("docker")


class RootlessDockerInstaller(Installer):
    name = "docker-rootless"

    def install(self):
        apt_install("uidmap")

        # Disable root service
        cmd("systemctl disable --now docker.service docker.socket", sudo=True)

        # Run install script from /usr/bin
        cmd("dockerd-rootless-setuptool.sh install")

        # Run on startup
        cmd("systemctl --user enable docker")
        cmd(f"loginctl enable-linger {env.USERNAME}", sudo=True)

        # Allow privileged ports
        # Use `slirp4netns` so that client IP addresses can be seen by containers for logging.
        #  - see https://docs.docker.com/engine/security/rootless/#networking-errors
        override_dir = env.homedir(".config/systemd/user/docker.service.d")
        mkdir(override_dir)
        copy_file(
            "files/docker-privileged-ports.conf",
            f"{override_dir}/override.conf",
        )
        cmd(
            "echo 'net.ipv4.ip_unprivileged_port_start=0' >> /etc/sysctl.conf",
            sudo=True,
        )

        cmd("sysctl --system", sudo=True)
        cmd("systemctl --user daemon-reload")
        cmd("systemctl --user restart docker")

    def is_installed(self) -> bool:
        return os.path.exists(
            env.homedir(".config/systemd/user/docker.service.d/override.conf")
        )
