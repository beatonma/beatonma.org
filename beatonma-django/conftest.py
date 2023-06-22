def pytest_addoption(parser):
    parser.addoption("--network", action="store_true", default=False)
