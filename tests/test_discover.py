from pathlib import Path

import pytest

from fastapi_cli.discover import (
    ImportData,
    get_import_data_from_import_string,
)
from fastapi_cli.exceptions import FastAPICLIException

assets_path = Path(__file__).parent / "assets"


def test_get_import_data_from_import_string_valid() -> None:
    result = get_import_data_from_import_string("module.submodule:app")

    assert isinstance(result, ImportData)
    assert result.app_name == "app"
    assert result.import_string == "module.submodule:app"
    assert result.module_data.module_import_str == "module.submodule"
    assert result.module_data.extra_sys_path == Path(".").resolve()
    assert result.module_data.module_paths == []


def test_get_import_data_from_import_string_missing_colon() -> None:
    with pytest.raises(FastAPICLIException) as exc_info:
        get_import_data_from_import_string("module.submodule")

    assert "Import string must be in the format module.submodule:app_name" in str(
        exc_info.value
    )


def test_get_import_data_from_import_string_missing_app() -> None:
    with pytest.raises(FastAPICLIException) as exc_info:
        get_import_data_from_import_string("module.submodule:")

    assert "Import string must be in the format module.submodule:app_name" in str(
        exc_info.value
    )


def test_get_import_data_from_import_string_missing_module() -> None:
    with pytest.raises(FastAPICLIException) as exc_info:
        get_import_data_from_import_string(":app")

    assert "Import string must be in the format module.submodule:app_name" in str(
        exc_info.value
    )


def test_get_import_data_from_import_string_empty() -> None:
    with pytest.raises(FastAPICLIException) as exc_info:
        get_import_data_from_import_string("")

    assert "Import string must be in the format module.submodule:app_name" in str(
        exc_info.value
    )
