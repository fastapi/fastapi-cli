from pathlib import Path

import pytest
from pytest import CaptureFixture

from fastapi_cli.discover import get_import_data
from fastapi_cli.exceptions import FastAPICLIException
from tests.utils import changing_dir

assets_path = Path(__file__).parent / "assets"


def test_package_app_root() -> None:
    with changing_dir(assets_path):
        import_data = get_import_data(path=Path("package/mod/app.py"))

    assert import_data.import_string == "package.mod.app:app"

    assert import_data.module_data.extra_sys_path == assets_path
    assert import_data.module_data.module_import_str == "package.mod.app"


def test_package_api_root() -> None:
    with changing_dir(assets_path):
        import_data = get_import_data(path=Path("package/mod/api.py"))

    assert import_data.import_string == "package.mod.api:api"

    assert import_data.module_data.extra_sys_path == assets_path
    assert import_data.module_data.module_import_str == "package.mod.api"


def test_package_other_root() -> None:
    with changing_dir(assets_path):
        import_data = get_import_data(path=Path("package/mod/other.py"))

    assert import_data.import_string == "package.mod.other:first_other"

    assert import_data.module_data.extra_sys_path == assets_path
    assert import_data.module_data.module_import_str == "package.mod.other"


def test_package_app_mod() -> None:
    with changing_dir(assets_path / "package/mod"):
        import_data = get_import_data(path=Path("app.py"))

    assert import_data.import_string == "package.mod.app:app"

    assert import_data.module_data.extra_sys_path == assets_path
    assert import_data.module_data.module_import_str == "package.mod.app"


def test_package_api_mod() -> None:
    with changing_dir(assets_path / "package/mod"):
        import_data = get_import_data(path=Path("api.py"))

    assert import_data.import_string == "package.mod.api:api"

    assert import_data.module_data.extra_sys_path == assets_path
    assert import_data.module_data.module_import_str == "package.mod.api"


def test_package_other_mod() -> None:
    with changing_dir(assets_path / "package/mod"):
        import_data = get_import_data(path=Path("other.py"))

    assert import_data.import_string == "package.mod.other:first_other"

    assert import_data.module_data.extra_sys_path == assets_path
    assert import_data.module_data.module_import_str == "package.mod.other"


def test_package_app_above() -> None:
    with changing_dir(assets_path.parent):
        import_data = get_import_data(path=Path("assets/package/mod/app.py"))

    assert import_data.import_string == "package.mod.app:app"

    assert import_data.module_data.extra_sys_path == assets_path
    assert import_data.module_data.module_import_str == "package.mod.app"


def test_package_api_parent() -> None:
    with changing_dir(assets_path.parent):
        import_data = get_import_data(path=Path("assets/package/mod/api.py"))

    assert import_data.import_string == "package.mod.api:api"

    assert import_data.module_data.extra_sys_path == assets_path
    assert import_data.module_data.module_import_str == "package.mod.api"


def test_package_other_parent() -> None:
    with changing_dir(assets_path.parent):
        import_data = get_import_data(path=Path("assets/package/mod/other.py"))

    assert import_data.import_string == "package.mod.other:first_other"

    assert import_data.module_data.extra_sys_path == assets_path
    assert import_data.module_data.module_import_str == "package.mod.other"


def test_package_mod_init_inside() -> None:
    with changing_dir(assets_path / "package/mod"):
        import_data = get_import_data(path=Path("__init__.py"))
        assert import_data.import_string == "package.mod:app"

    assert import_data.module_data.extra_sys_path == assets_path
    assert import_data.module_data.module_import_str == "package.mod"


def test_package_mod_dir() -> None:
    with changing_dir(assets_path):
        import_data = get_import_data(path=Path("package/mod"))

    assert import_data.import_string == "package.mod:app"

    assert import_data.module_data.extra_sys_path == assets_path
    assert import_data.module_data.module_import_str == "package.mod"


def test_package_init_inside() -> None:
    with changing_dir(assets_path / "package"):
        import_data = get_import_data(path=Path("__init__.py"))

    assert import_data.import_string == "package:app"

    assert import_data.module_data.extra_sys_path == assets_path
    assert import_data.module_data.module_import_str == "package"


def test_package_dir_inside_package() -> None:
    with changing_dir(assets_path / "package/mod"):
        import_data = get_import_data(path=Path("../"))

    assert import_data.import_string == "package:app"
    assert import_data.module_data.extra_sys_path == assets_path
    assert import_data.module_data.module_import_str == "package"


def test_package_dir_above_package() -> None:
    with changing_dir(assets_path.parent):
        import_data = get_import_data(path=Path("assets/package"))

    assert import_data.import_string == "package:app"

    assert import_data.module_data.extra_sys_path == assets_path
    assert import_data.module_data.module_import_str == "package"


def test_package_dir_explicit_app() -> None:
    with changing_dir(assets_path):
        import_data = get_import_data(path=Path("package"), app_name="api")

    assert import_data.import_string == "package:api"

    assert import_data.module_data.extra_sys_path == assets_path
    assert import_data.module_data.module_import_str == "package"


def test_broken_package_dir(capsys: CaptureFixture[str]) -> None:
    with changing_dir(assets_path):
        # TODO (when deprecating Python 3.8): remove ValueError
        with pytest.raises((ImportError, ValueError)):
            get_import_data(path=Path("broken_package/mod/app.py"))

    captured = capsys.readouterr()
    assert "Import error:" in captured.out
    assert "Ensure all the package directories have an __init__.py file" in captured.out


def test_package_dir_no_app() -> None:
    with changing_dir(assets_path):
        with pytest.raises(FastAPICLIException) as e:
            get_import_data(path=Path("package/core/utils.py"))
        assert (
            "Could not find FastAPI app in module, try using --app" in e.value.args[0]
        )


def test_package_dir_object_not_an_app() -> None:
    with changing_dir(assets_path):
        with pytest.raises(FastAPICLIException) as e:
            get_import_data(
                path=Path("package/core/utils.py"), app_name="get_hello_world"
            )
        assert (
            "The app name get_hello_world in package.core.utils doesn't seem to be a FastAPI app"
            in e.value.args[0]
        )


def test_package_dir_object_app_name_not_found() -> None:
    with changing_dir(assets_path):
        with pytest.raises(FastAPICLIException) as e:
            get_import_data(path=Path("package"), app_name="non_existent_app")
        assert "Could not find app name non_existent_app in package" in e.value.args[0]
