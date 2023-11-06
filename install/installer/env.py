import logging
import os
from pathlib import Path


def get_logger(name: str) -> logging.Logger:
    _log = logging.getLogger(name)
    _log.setLevel(logging.DEBUG)
    _log.addHandler(logging.StreamHandler())
    return _log


log = get_logger(__name__)
DOTENV_KEYS = ["HOST_USERNAME", "HOST_SAMBA_PASSWORD", "HOST_SSH_PASSWORD"]

os.chdir(Path(__file__).parent.parent)
DOTENV_FILE = Path.cwd() / ".env"

if not DOTENV_FILE.exists():
    raise EnvironmentError(".env file not found in 'install' directory")

_env = {}
with open(DOTENV_FILE, "r") as dotenv:
    for line in dotenv.readlines():
        line = line.strip()
        if line.startswith("#"):
            continue

        if line.count("=") != 1:
            continue

        key, value = line.split("=")
        _env[key] = value

    for key in DOTENV_KEYS:
        if key not in _env:
            raise EnvironmentError(f"Expected environment variable '{key}' is missing.")

USERNAME = _env["HOST_USERNAME"]
SAMBA_PASS = _env["HOST_SAMBA_PASSWORD"]
SSH_PASS = _env["HOST_SSH_PASSWORD"]
HOME_DIR = Path(f"/home/{USERNAME}")
del _env, DOTENV_KEYS, DOTENV_FILE


def homedir(path: str = "") -> Path:
    return HOME_DIR / path
