from pathlib import Path

import pytest
from fastapi_cli.discover import get_import_string
from fastapi_cli.exceptions import FastAPICLIException
from pytest import CaptureFixture

assets_path = Path(__file__).parent / "assets"


@pytest.mark.parametrize(
    (
        "chdir_path",
        "import_path",
        "app_name",
        "expect_import_string",
    ),
    [
        ("package/mod", "__init__.py", None, "package.mod:app"),
        ("package", "__init__.py", None, "package:app"),
        ("package/mod", "../", None, "package:app"),
        ("..", "assets/package", None, "package:app"),
        ("", "package", "api", "package:api"),
        ("..", "assets/package/mod/app.py", None, "package.mod.app:app"),
        ("..", "assets/package/mod/api.py", None, "package.mod.api:api"),
        ("..", "assets/package/mod/other.py", None, "package.mod.other:first_other"),
        ("package/mod", "app.py", None, "package.mod.app:app"),
        ("package/mod", "api.py", None, "package.mod.api:api"),
        ("package/mod", "other.py", None, "package.mod.other:first_other"),
        ("", "package/mod/app.py", None, "package.mod.app:app"),
        ("", "package/mod/api.py", None, "package.mod.api:api"),
        ("", "package/mod/other.py", None, "package.mod.other:first_other"),
    ],
)
def test_package_mod_init_inside(
    chdir_path,
    import_path,
    app_name,
    expect_import_string,
    monkeypatch: pytest.MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    monkeypatch.chdir(assets_path / chdir_path)

    import_path = Path(import_path)
    import_string = get_import_string(path=Path(import_path), app_name=app_name)
    assert import_string == expect_import_string

    module_name, app_name = import_string.split(":")
    module_path = module_name.split(".")

    captured = capsys.readouterr()
    assert f"Using path {import_path}" in captured.out
    assert "Resolved absolute path" in captured.out
    assert f"{Path(import_path).resolve()}" in captured.out
    assert (
        "Searching for package file structure from directories with __init__.py files"
        in captured.out
    )
    assert "Importing from" in captured.out
    assert "tests/assets" in captured.out
    assert "╭─ Python package file structure ─╮" in captured.out
    assert f"  📁 {module_path[0]}" in captured.out
    if len(module_path) == 1:
        assert "  └── 🐍 __init__.py" in captured.out
    else:
        assert "  ├── 🐍 __init__.py" in captured.out
        assert f"  └── 📁 {module_path[1]}" in captured.out
        if import_path.name != "__init__.py":
            assert "    ├── 🐍 __init__.py " in captured.out
            assert f"    └── 🐍 {import_path.name}" in captured.out
        else:
            assert "    └── 🐍 __init__.py " in captured.out
    assert f"Importing module {module_name}" in captured.out
    assert "Found importable FastAPI app" in captured.out
    assert "Importable FastAPI app" in captured.out
    assert f"from {module_name} import {app_name}" in captured.out
    assert f"Using import string {module_name}:{app_name}" in captured.out


def test_broken_package_dir(
    monkeypatch: pytest.MonkeyPatch, capsys: CaptureFixture[str]
) -> None:
    monkeypatch.chdir(assets_path)
    # TODO (when deprecating Python 3.8): remove ValueError
    with pytest.raises((ImportError, ValueError)):
        get_import_string(path=Path("broken_package/mod/app.py"))

    captured = capsys.readouterr()
    assert "Import error:" in captured.out
    assert "Ensure all the package directories have an __init__.py file" in captured.out


def test_package_dir_no_app(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(assets_path)
    with pytest.raises(FastAPICLIException) as e:
        get_import_string(path=Path("package/core/utils.py"))
    assert "Could not find FastAPI app in module, try using --app" in e.value.args[0]


def test_package_dir_object_not_an_app(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(assets_path)
    with pytest.raises(FastAPICLIException) as e:
        get_import_string(
            path=Path("package/core/utils.py"), app_name="get_hello_world"
        )
    assert (
        "The app name get_hello_world in package.core.utils doesn't seem to be a FastAPI app"
        in e.value.args[0]
    )


def test_package_dir_object_app_name_not_found(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(assets_path)
    with pytest.raises(FastAPICLIException) as e:
        get_import_string(path=Path("package"), app_name="non_existent_app")
    assert "Could not find app name non_existent_app in package" in e.value.args[0]
