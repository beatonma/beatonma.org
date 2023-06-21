"""Each submodule should define a `test()` function."""
import pkgutil
import sys
from typing import Dict, Optional

results: Dict[str, Optional[Exception]] = {}
all_ok = True

for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
    module_ = loader.find_module(module_name).load_module(module_name)
    testfunc = getattr(module_, "tests")
    print(f"Testing {module_.__name__}…")
    try:
        testfunc()
        results[module_name] = None
    except AssertionError as e:
        results[module_name] = e
        all_ok = False


sorted_results = sorted(results.items(), key=lambda x: x is None)
for module_name, error in sorted_results:
    result_code = "OK" if error is None else "FAIL"
    print(f"[{result_code}] {module_name}")

    if error:
        print(f"- {error}")

if not all_ok:
    sys.exit(1)
