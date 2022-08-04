from typing import Any, NoReturn
import pytest
import shutil
import os
from ... import utils
from .cli_env import cli_env  # noqa


@pytest.fixture(scope="session")
def cli_env_root_dir(tmpdir_factory: pytest.TempdirFactory) -> str:
    root_dir = str(tmpdir_factory.mktemp("_scr_cli_env"))
    # we need the resources for the tests to be available as relative paths
    # like ../res/a.txt
    res_dir = os.path.join(os.path.dirname(__file__), "res")
    res_tgt = os.path.join(root_dir, "res")
    try:
        os.symlink(res_dir, res_tgt)
    except OSError:
        assert utils.is_windows()
        # for whatever reason, windows doesn't allow us to create symlinks
        # unless we're in 'developer mode' or some BS like that, so we copy
        # the whole res folder, which is luckily not that big
        shutil.copytree(res_dir, res_tgt)
    return root_dir


# this makes sure that exceptions in tests are raise properly
# see https://stackoverflow.com/questions/62419998/how-can-i-get-pytest-to-not-catch-exceptions
if __debug__:
    @pytest.hookimpl(tryfirst=True)  # type: ignore
    def pytest_exception_interact(call: Any) -> NoReturn:
        raise call.excinfo.value

    @pytest.hookimpl(tryfirst=True)  # type: ignore
    def pytest_internalerror(excinfo: Any) -> NoReturn:
        raise excinfo.value
