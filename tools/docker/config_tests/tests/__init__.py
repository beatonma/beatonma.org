import importlib.machinery
import importlib.util
import logging
import pkgutil
import sys
from pathlib import Path

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler())

RESULT_OK = "OK"
RESULT_FAIL = "FAIL"
MAX_RESULT_LENGTH = max(len(RESULT_OK), len(RESULT_FAIL))


def log_result_message(result: str, message: str):
    return f"{result.ljust(MAX_RESULT_LENGTH)} {message}"


def result_ok(message: str):
    return log.info(log_result_message(RESULT_OK, message))


def result_fail(message: str):
    return log.warning(log_result_message(RESULT_FAIL, message))


def run_tests():
    results: dict[str, Exception | None] = {}
    all_ok = True
    for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
        _loader = importlib.machinery.SourceFileLoader(
            module_name, str(Path(loader.path) / f"{module_name}.py")
        )
        spec = importlib.util.spec_from_loader(module_name, _loader)

        module = importlib.util.module_from_spec(spec)
        _loader.exec_module(module)

        for name, obj in module.__dict__.items():
            if callable(obj) and name.startswith("test_"):
                fullname = f"{module_name}.{obj.__name__}"
                try:
                    obj()
                    result_ok(fullname)
                except AssertionError as e:
                    result_fail(fullname)
                    results[fullname] = e
                    all_ok = False

    if not all_ok:
        log.error("\nExceptions:\n")
        for module, exception in results.items():
            log.error(f"{module}:\n{exception}\n\n")

        sys.exit(1)


run_tests()
