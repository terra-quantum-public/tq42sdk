from pytest import mark
from tq42.functional_tests.functional_test_config import FunctionalTestConfig


def pytest_addoption(parser):
    parser.addoption(
        "--poll", action="store_true", default=False, help="run polling tests"
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption("--poll"):
        return
    skip_poll = mark.skip(reason="need --poll option to run")
    for item in items:
        if "poll" in item.keywords:
            item.add_marker(skip_poll)


FunctionalTestConfig.args = FunctionalTestConfig.prepare_defaults()
