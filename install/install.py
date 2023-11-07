from installer import env
from installer.components import (
    BashRcInstaller,
    CronInstaller,
    DockerInstaller,
    Fail2BanInstaller,
    FilesystemInstaller,
    GitInstaller,
    RootlessDockerInstaller,
    SambaInstaller,
)
from installer.components.installer import Installer
from installer.shell import cmd

log = env.get_logger(__name__)


def install_component(component: Installer) -> bool:
    if component.is_installed():
        log.info(f"Component '{component.name}' is ready.")
        return False

    log.info(f"Installing component '{component.name}'...")
    component.install()

    if not component.is_installed():
        raise Exception(
            f"Installation error: {component.name}.install() completed but is_installed() still returns False!"
        )

    log.info(f"Successfully configured component '{component.name}'")
    return True


def preinstall_docker():
    installer = DockerInstaller()

    was_installed = install_component(installer)

    if was_installed:
        log.warning(
            "Docker has been installed successfully. "
            "Please restart the system, then run the installer again."
        )
        exit(0)


def main():
    preinstall_docker()

    installers = [
        FilesystemInstaller,
        GitInstaller,
        BashRcInstaller,
        CronInstaller,
        Fail2BanInstaller,
        SambaInstaller,
        RootlessDockerInstaller,
    ]
    for component_class in installers:
        component = component_class()
        install_component(component)

    log.info("All components installed!")
    for component_class in installers:
        log.info(f"- {component_class.name}")

    cmd("./bma certbot init")

    log.info("System setup complete!")
    log.info("Next steps:")
    log.info("> eval $(ssh-agent -s && ssh-add")
    log.info("> ./bma production build")
    log.info("> ./bma production up -d")
    log.info("> ./bma import path/to/archive.tar.gz")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit(1)
