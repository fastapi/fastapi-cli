from pathlib import Path

import pytest

from fastapi_cli.discover import get_import_data
from fastapi_cli.exceptions import FastAPICLIException

from .utils import changing_dir

assets_path = Path(__file__).parent / "assets"


def test_app_dir_main() -> None:
    dir = assets_path / "default_files" / "default_app_dir_main"
    with changing_dir(dir):
        import_data = get_import_data()

    assert import_data.import_string == "app.main:app"

    assert import_data.module_data.extra_sys_path == dir
    assert import_data.module_data.module_import_str == "app.main"


def test_app_dir_app() -> None:
    dir = assets_path / "default_files" / "default_app_dir_app"
    with changing_dir(dir):
        import_data = get_import_data()

    assert import_data.import_string == "app.app:app"

    assert import_data.module_data.extra_sys_path == dir
    assert import_data.module_data.module_import_str == "app.app"


def test_app_dir_api() -> None:
    dir = assets_path / "default_files" / "default_app_dir_api"
    with changing_dir(dir):
        import_data = get_import_data()

    assert import_data.import_string == "app.api:app"

    assert import_data.module_data.extra_sys_path == dir
    assert import_data.module_data.module_import_str == "app.api"


def test_app_dir_non_default() -> None:
    with changing_dir(assets_path / "default_files" / "default_app_dir_non_default"):
        with pytest.raises(FastAPICLIException) as e:
            get_import_data()
        assert (
            "Could not find a default file to run, please provide an explicit path"
            in e.value.args[0]
        )
