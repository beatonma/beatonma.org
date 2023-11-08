import os
from argparse import ArgumentParser

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

INSTALLERS = [
    FilesystemInstaller,
    GitInstaller,
    BashRcInstaller,
    CronInstaller,
    Fail2BanInstaller,
    SambaInstaller,
    RootlessDockerInstaller,
]


def parse_args():
    parser = ArgumentParser()

    parser.add_argument(
        "--component", type=str, choices=list(map(lambda x: x.name, INSTALLERS))
    )

    return parser.parse_args()


def install_component(component: Installer, force: bool = False) -> bool:
    if (not force) and component.is_installed():
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


def reinstall_component(component_name: str):
    for inst in INSTALLERS:
        if component_name == inst.name:
            log.info(f"Force-installing component '{component_name}'")
            component = inst()
            install_component(component, force=True)
            return
    else:
        log.warning(f"Unknown component '{component_name}'")


def complete_install():
    preinstall_docker()

    for component_class in INSTALLERS:
        component = component_class()
        install_component(component)

    log.info("All components installed!")
    for component_class in INSTALLERS:
        log.info(f"- {component_class.name}")

    log.info("System setup complete!")
    log.info("Next steps:")
    log.info("> ./bma certbot init")
    log.info("> eval $(ssh-agent -s && ssh-add")
    log.info("> ./bma production build")
    log.info("> ./bma production up -d")
    log.info("> ./bma import path/to/archive.tar.gz")


def main():
    args = parse_args()

    if args.component:
        return reinstall_component(args.component)

    complete_install()


if __name__ == "__main__":
    main()
