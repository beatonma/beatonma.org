import shutil
import subprocess
from dataclasses import dataclass, field
from functools import reduce
from pathlib import Path
from typing import List, Optional

from .env import get_logger

log = get_logger(__name__)


@dataclass
class Result:
    command: str
    output: str
    code: Optional[int]
    inputs: Optional[List[str]] = None
    successful: bool = field(init=False)

    def __post_init__(self):
        self.successful = self.code is None
        if self.output:
            log.debug(self.output)

    def __iadd__(self, other: "Result"):
        inputs = (self.inputs or []) + (other.inputs or [])
        output = [x for x in [self.output, other.output] if x]
        return Result(
            f"{self.command} | {other.command}",
            output="\n---\n".join(output) if output else "",
            code=self.code or other.code,
            inputs=inputs or None,
        )


def cmd(
    command: str,
    inputs: List[str] = None,
    sudo: bool = False,
    throw: bool = True,
) -> Result:
    if sudo:
        command = f"sudo {command}"

    log.info(f"> {command}")

    process = subprocess.Popen(
        command,
        shell=True,
        text=True,
        stdin=subprocess.PIPE if inputs else None,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if inputs:
        for value in inputs:
            process.stdin.write(f"{value}\n")
            log.info(f" > {value}")

    stdout, stderr = process.communicate()
    result_code = process.returncode
    output = stdout if result_code == 0 else stderr

    if process.stdin:
        process.stdin.close()
    process.stdout.close()
    process.stderr.close()

    if throw and result_code != 0:
        raise IOError(
            f"run_command error: '{command}' return code={result_code} | {output}"
        )

    return Result(command=command, output=output, code=result_code)


def apt_update() -> Result:
    return cmd("apt update", sudo=True)


def apt_install(*packages) -> Result:
    return cmd(f"apt install -y {' '.join(packages)}", sudo=True)


def is_installed(*packages) -> bool:
    return reduce(
        lambda b, value: value and b,
        [shutil.which(package) is not None for package in packages],
        True,
    )


def write_file(path: str, content: str, sudo: bool = False) -> Result:
    tee = f"tee"
    if sudo:
        tee = f"sudo {tee}"
    return cmd(f"echo '{content}' | {tee} {path}", sudo=sudo)


def mkdir(
    path: str | Path,
    sudo: bool = False,
    mode: int = None,
    owner: str = None,
    throw: bool = True,
) -> Result:
    result = cmd(f"mkdir -p {path}", sudo=sudo, throw=throw)

    if owner:
        result += chown(owner, path, sudo=sudo, throw=throw)
    if mode:
        result += chmod(mode, path, sudo=sudo, throw=throw)

    return result


def chown(
    user: str,
    path: str | Path,
    group: str = None,
    sudo: bool = False,
    throw: bool = True,
) -> Result:
    if not group:
        group = user
    return cmd(f"chown {user}:{group} {path}", sudo=sudo, throw=throw)


def chmod(
    mode: int, path: str | Path, sudo: bool = False, throw: bool = True
) -> Result:
    return cmd(f"chmod {mode} {path}", sudo=sudo, throw=throw)


def copy_file(
    source: str | Path, target: str | Path, sudo: bool = False, throw: bool = True
) -> Result:
    return cmd(
        f"cp -r {Path.cwd() / source} {target}",
        sudo=sudo,
        throw=throw,
    )


def tree(path: str | Path) -> Result:
    return cmd(f"tree {path}")
