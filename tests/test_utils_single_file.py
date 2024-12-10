from pathlib import Path

import pytest
from pytest import CaptureFixture

from fastapi_cli.discover import get_import_data
from fastapi_cli.exceptions import FastAPICLIException

from .utils import changing_dir

assets_path = Path(__file__).parent / "assets"


def test_single_file_app(capsys: CaptureFixture[str]) -> None:
    with changing_dir(assets_path):
        import_data = get_import_data(path=Path("single_file_app.py"))

    assert import_data.import_string == "single_file_app:app"

    assert import_data.module_data.extra_sys_path == assets_path
    assert import_data.module_data.module_import_str == "single_file_app"


def test_single_file_api(capsys: CaptureFixture[str]) -> None:
    with changing_dir(assets_path):
        import_data = get_import_data(path=Path("single_file_api.py"))

    assert import_data.import_string == "single_file_api:api"

    assert import_data.module_data.extra_sys_path == assets_path
    assert import_data.module_data.module_import_str == "single_file_api"


def test_single_file_other(capsys: CaptureFixture[str]) -> None:
    with changing_dir(assets_path):
        import_data = get_import_data(path=Path("single_file_other.py"))

    assert import_data.import_string == "single_file_other:first_other"

    assert import_data.module_data.extra_sys_path == assets_path
    assert import_data.module_data.module_import_str == "single_file_other"


def test_single_file_explicit_object(capsys: CaptureFixture[str]) -> None:
    with changing_dir(assets_path):
        import_data = get_import_data(
            path=Path("single_file_app.py"), app_name="second_other"
        )

    assert import_data.import_string == "single_file_app:second_other"

    assert import_data.module_data.extra_sys_path == assets_path
    assert import_data.module_data.module_import_str == "single_file_app"


def test_single_non_existing_file() -> None:
    with changing_dir(assets_path):
        with pytest.raises(FastAPICLIException) as e:
            get_import_data(path=assets_path / "non_existing.py")
    assert "Path does not exist" in e.value.args[0]
