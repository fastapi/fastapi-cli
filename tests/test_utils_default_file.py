import importlib
import sys
from pathlib import Path

import pytest
from pytest import CaptureFixture

from fastapi_cli.discover import get_import_data
from fastapi_cli.exceptions import FastAPICLIException

from .utils import changing_dir

assets_path = Path(__file__).parent / "assets"


def test_single_file_main() -> None:
    root_path = assets_path / "default_files" / "default_main"
    old_sys_path = sys.path.copy()
    with changing_dir(root_path):
        sys.path.insert(0, str(root_path))
        mod = importlib.import_module("main")

        importlib.reload(mod)
        import_data = get_import_data()

    assert import_data.import_string == "main:app"
    assert import_data.module_data.extra_sys_path == root_path
    assert import_data.module_data.module_import_str == "main"

    sys.path = old_sys_path


def test_single_file_app() -> None:
    root_path = assets_path / "default_files" / "default_app"
    old_sys_path = sys.path.copy()
    with changing_dir(root_path):
        sys.path.insert(0, str(root_path))
        mod = importlib.import_module("app")

        importlib.reload(mod)
        import_data = get_import_data()

    assert import_data.import_string == "app:app"
    assert import_data.module_data.extra_sys_path == root_path
    assert import_data.module_data.module_import_str == "app"

    sys.path = old_sys_path


def test_single_file_api() -> None:
    root_path = assets_path / "default_files" / "default_api"
    old_sys_path = sys.path.copy()
    with changing_dir(root_path):
        sys.path.insert(0, str(root_path))
        mod = importlib.import_module("api")

        importlib.reload(mod)
        import_data = get_import_data()

    assert import_data.import_string == "api:app"
    assert import_data.module_data.extra_sys_path == root_path
    assert import_data.module_data.module_import_str == "api"

    sys.path = old_sys_path


def test_non_default_file(capsys: CaptureFixture[str]) -> None:
    with changing_dir(assets_path / "default_files" / "non_default"):
        with pytest.raises(FastAPICLIException) as e:
            get_import_data()
        assert (
            "Could not find a default file to run, please provide an explicit path"
            in e.value.args[0]
        )
