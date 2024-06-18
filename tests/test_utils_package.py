from pathlib import Path

import pytest
from fastapi_cli.discover import get_import_string
from fastapi_cli.exceptions import FastAPICLIException
from pytest import CaptureFixture

from tests.utils import changing_dir

assets_path = Path(__file__).parent / "assets"


def test_package_app_root(capsys: CaptureFixture[str]) -> None:
    with changing_dir(assets_path):
        import_string, is_factory = get_import_string(path=Path("package/mod/app.py"))
        assert import_string == "package.mod.app:app"
        assert is_factory is False

    captured = capsys.readouterr()
    assert "Using path package/mod/app.py" in captured.out
    assert "Resolved absolute path" in captured.out
    assert "tests/assets/package/mod/app.py" in captured.out
    assert (
        "Searching for package file structure from directories with __init__.py files"
        in captured.out
    )
    assert "Importing from" in captured.out
    assert "tests/assets" in captured.out
    assert "╭─ Python package file structure ─╮" in captured.out
    assert "│  📁 package" in captured.out
    assert "│  ├── 🐍 __init__.py" in captured.out
    assert "│  └── 📁 mod" in captured.out
    assert "│      ├── 🐍 __init__.py " in captured.out
    assert "│      └── 🐍 app.py" in captured.out
    assert "Importing module package.mod.app" in captured.out
    assert "Found importable FastAPI app" in captured.out
    assert "Importable FastAPI app" in captured.out
    assert "from package.mod.app import app" in captured.out
    assert "Using import string package.mod.app:app" in captured.out


def test_package_api_root(capsys: CaptureFixture[str]) -> None:
    with changing_dir(assets_path):
        import_string, is_factory = get_import_string(path=Path("package/mod/api.py"))
        assert import_string == "package.mod.api:api"
        assert is_factory is False

    captured = capsys.readouterr()
    assert "Using path package/mod/api.py" in captured.out
    assert "Resolved absolute path" in captured.out
    assert "tests/assets/package/mod/api.py" in captured.out
    assert (
        "Searching for package file structure from directories with __init__.py files"
        in captured.out
    )
    assert "Importing from" in captured.out
    assert "tests/assets" in captured.out
    assert "╭─ Python package file structure ─╮" in captured.out
    assert "│  📁 package" in captured.out
    assert "│  ├── 🐍 __init__.py" in captured.out
    assert "│  └── 📁 mod" in captured.out
    assert "│      ├── 🐍 __init__.py " in captured.out
    assert "│      └── 🐍 api.py" in captured.out
    assert "Importing module package.mod.api" in captured.out
    assert "Found importable FastAPI app" in captured.out
    assert "Importable FastAPI app" in captured.out
    assert "from package.mod.api import api" in captured.out
    assert "Using import string package.mod.api:api" in captured.out


def test_package_other_root(capsys: CaptureFixture[str]) -> None:
    with changing_dir(assets_path):
        import_string, is_factory = get_import_string(path=Path("package/mod/other.py"))
        assert import_string == "package.mod.other:first_other"
        assert is_factory is False

    captured = capsys.readouterr()
    assert "Using path package/mod/other.py" in captured.out
    assert "Resolved absolute path" in captured.out
    assert "tests/assets/package/mod/other.py" in captured.out
    assert (
        "Searching for package file structure from directories with __init__.py files"
        in captured.out
    )
    assert "Importing from" in captured.out
    assert "tests/assets" in captured.out
    assert "╭─ Python package file structure ─╮" in captured.out
    assert "│  📁 package" in captured.out
    assert "│  ├── 🐍 __init__.py" in captured.out
    assert "│  └── 📁 mod" in captured.out
    assert "│      ├── 🐍 __init__.py " in captured.out
    assert "│      └── 🐍 other.py" in captured.out
    assert "Importing module package.mod.other" in captured.out
    assert "Found importable FastAPI app" in captured.out
    assert "Importable FastAPI app" in captured.out
    assert "from package.mod.other import first_other" in captured.out
    assert "Using import string package.mod.other:first_other" in captured.out


def test_package_factory_app_root(capsys: CaptureFixture[str]) -> None:
    with changing_dir(assets_path):
        import_string, is_factory = get_import_string(
            path=Path("package/mod/factory_app.py")
        )
        assert import_string == "package.mod.factory_app:create_app"
        assert is_factory is True

    captured = capsys.readouterr()
    assert "Using path package/mod/factory_app.py" in captured.out
    assert "Resolved absolute path" in captured.out
    assert "tests/assets/package/mod/factory_app.py" in captured.out
    assert (
        "Searching for package file structure from directories with __init__.py files"
        in captured.out
    )
    assert "Importing from" in captured.out
    assert "tests/assets" in captured.out
    assert "╭─ Python package file structure ─╮" in captured.out
    assert "│  📁 package" in captured.out
    assert "│  ├── 🐍 __init__.py" in captured.out
    assert "│  └── 📁 mod" in captured.out
    assert "│      ├── 🐍 __init__.py " in captured.out
    assert "│      └── 🐍 factory_app.py" in captured.out
    assert "Importing module package.mod.factory_app" in captured.out
    assert "Found importable FastAPI app" in captured.out
    assert "Importable FastAPI app" in captured.out
    assert "from package.mod.factory_app import create_app" in captured.out
    assert "Using import string package.mod.factory_app:create_app" in captured.out


def test_package_factory_api_root(capsys: CaptureFixture[str]) -> None:
    with changing_dir(assets_path):
        import_string, is_factory = get_import_string(
            path=Path("package/mod/factory_api.py")
        )
        assert import_string == "package.mod.factory_api:create_api"
        assert is_factory is True

    captured = capsys.readouterr()
    assert "Using path package/mod/factory_api.py" in captured.out
    assert "Resolved absolute path" in captured.out
    assert "tests/assets/package/mod/factory_api.py" in captured.out
    assert (
        "Searching for package file structure from directories with __init__.py files"
        in captured.out
    )
    assert "Importing from" in captured.out
    assert "tests/assets" in captured.out
    assert "╭─ Python package file structure ─╮" in captured.out
    assert "│  📁 package" in captured.out
    assert "│  ├── 🐍 __init__.py" in captured.out
    assert "│  └── 📁 mod" in captured.out
    assert "│      ├── 🐍 __init__.py " in captured.out
    assert "│      └── 🐍 factory_api.py" in captured.out
    assert "Importing module package.mod.factory_api" in captured.out
    assert "Found importable FastAPI app" in captured.out
    assert "Importable FastAPI app" in captured.out
    assert "from package.mod.factory_api import create_api" in captured.out
    assert "Using import string package.mod.factory_api:create_api" in captured.out


def test_package_factory_other_root(capsys: CaptureFixture[str]) -> None:
    with changing_dir(assets_path):
        import_string, is_factory = get_import_string(
            path=Path("package/mod/factory_other.py"), app_name="build_app"
        )
        assert import_string == "package.mod.factory_other:build_app"
        assert is_factory is True

    captured = capsys.readouterr()
    assert "Using path package/mod/factory_other.py" in captured.out
    assert "Resolved absolute path" in captured.out
    assert "tests/assets/package/mod/factory_other.py" in captured.out
    assert (
        "Searching for package file structure from directories with __init__.py files"
        in captured.out
    )
    assert "Importing from" in captured.out
    assert "tests/assets" in captured.out
    assert "╭─ Python package file structure ─╮" in captured.out
    assert "│  📁 package" in captured.out
    assert "│  ├── 🐍 __init__.py" in captured.out
    assert "│  └── 📁 mod" in captured.out
    assert "│      ├── 🐍 __init__.py " in captured.out
    assert "│      └── 🐍 factory_other.py" in captured.out
    assert "Importing module package.mod.factory_other" in captured.out
    assert "Found importable FastAPI app" in captured.out
    assert "Importable FastAPI app" in captured.out
    assert "from package.mod.factory_other import build_app" in captured.out
    assert "Using import string package.mod.factory_other:build_app" in captured.out


def test_package_factory_inherit_root(capsys: CaptureFixture[str]) -> None:
    with changing_dir(assets_path):
        import_string, is_factory = get_import_string(
            path=Path("package/mod/factory_inherit.py")
        )
        assert import_string == "package.mod.factory_inherit:create_app"
        assert is_factory is True

    captured = capsys.readouterr()
    assert "Using path package/mod/factory_inherit.py" in captured.out
    assert "Resolved absolute path" in captured.out
    assert "tests/assets/package/mod/factory_inherit.py" in captured.out
    assert (
        "Searching for package file structure from directories with __init__.py files"
        in captured.out
    )
    assert "Importing from" in captured.out
    assert "tests/assets" in captured.out
    assert "╭─ Python package file structure ─╮" in captured.out
    assert "│  📁 package" in captured.out
    assert "│  ├── 🐍 __init__.py" in captured.out
    assert "│  └── 📁 mod" in captured.out
    assert "│      ├── 🐍 __init__.py " in captured.out
    assert "│      └── 🐍 factory_inherit.py" in captured.out
    assert "Importing module package.mod.factory_inherit" in captured.out
    assert "Found importable FastAPI app" in captured.out
    assert "Importable FastAPI app" in captured.out
    assert "from package.mod.factory_inherit import create_app" in captured.out
    assert "Using import string package.mod.factory_inherit:create_app" in captured.out


def test_package_app_mod(capsys: CaptureFixture[str]) -> None:
    with changing_dir(assets_path / "package/mod"):
        import_string, is_factory = get_import_string(path=Path("app.py"))
        assert import_string == "package.mod.app:app"
        assert is_factory is False

    captured = capsys.readouterr()
    assert "Using path app.py" in captured.out
    assert "Resolved absolute path" in captured.out
    assert "tests/assets/package/mod/app.py" in captured.out
    assert (
        "Searching for package file structure from directories with __init__.py files"
        in captured.out
    )
    assert "Importing from" in captured.out
    assert "tests/assets" in captured.out
    assert "╭─ Python package file structure ─╮" in captured.out
    assert "│  📁 package" in captured.out
    assert "│  ├── 🐍 __init__.py" in captured.out
    assert "│  └── 📁 mod" in captured.out
    assert "│      ├── 🐍 __init__.py " in captured.out
    assert "│      └── 🐍 app.py" in captured.out
    assert "Importing module package.mod.app" in captured.out
    assert "Found importable FastAPI app" in captured.out
    assert "Importable FastAPI app" in captured.out
    assert "from package.mod.app import app" in captured.out
    assert "Using import string package.mod.app:app" in captured.out


def test_package_api_mod(capsys: CaptureFixture[str]) -> None:
    with changing_dir(assets_path / "package/mod"):
        import_string, is_factory = get_import_string(path=Path("api.py"))
        assert import_string == "package.mod.api:api"
        assert is_factory is False

    captured = capsys.readouterr()
    assert "Using path api.py" in captured.out
    assert "Resolved absolute path" in captured.out
    assert "tests/assets/package/mod/api.py" in captured.out
    assert (
        "Searching for package file structure from directories with __init__.py files"
        in captured.out
    )
    assert "Importing from" in captured.out
    assert "tests/assets" in captured.out
    assert "╭─ Python package file structure ─╮" in captured.out
    assert "│  📁 package" in captured.out
    assert "│  ├── 🐍 __init__.py" in captured.out
    assert "│  └── 📁 mod" in captured.out
    assert "│      ├── 🐍 __init__.py " in captured.out
    assert "│      └── 🐍 api.py" in captured.out
    assert "Importing module package.mod.api" in captured.out
    assert "Found importable FastAPI app" in captured.out
    assert "Importable FastAPI app" in captured.out
    assert "from package.mod.api import api" in captured.out
    assert "Using import string package.mod.api:api" in captured.out


def test_package_other_mod(capsys: CaptureFixture[str]) -> None:
    with changing_dir(assets_path / "package/mod"):
        import_string, is_factory = get_import_string(path=Path("other.py"))
        assert import_string == "package.mod.other:first_other"
        assert is_factory is False

    captured = capsys.readouterr()
    assert "Using path other.py" in captured.out
    assert "Resolved absolute path" in captured.out
    assert "tests/assets/package/mod/other.py" in captured.out
    assert (
        "Searching for package file structure from directories with __init__.py files"
        in captured.out
    )
    assert "Importing from" in captured.out
    assert "tests/assets" in captured.out
    assert "╭─ Python package file structure ─╮" in captured.out
    assert "│  📁 package" in captured.out
    assert "│  ├── 🐍 __init__.py" in captured.out
    assert "│  └── 📁 mod" in captured.out
    assert "│      ├── 🐍 __init__.py " in captured.out
    assert "│      └── 🐍 other.py" in captured.out
    assert "Importing module package.mod.other" in captured.out
    assert "Found importable FastAPI app" in captured.out
    assert "Importable FastAPI app" in captured.out
    assert "from package.mod.other import first_other" in captured.out
    assert "Using import string package.mod.other:first_other" in captured.out


def test_package_factory_app_mod(capsys: CaptureFixture[str]) -> None:
    with changing_dir(assets_path / "package/mod"):
        import_string, is_factory = get_import_string(path=Path("factory_app.py"))
        assert import_string == "package.mod.factory_app:create_app"
        assert is_factory is True

    captured = capsys.readouterr()
    assert "Using path factory_app.py" in captured.out
    assert "Resolved absolute path" in captured.out
    assert "tests/assets/package/mod/factory_app.py" in captured.out
    assert (
        "Searching for package file structure from directories with __init__.py files"
        in captured.out
    )
    assert "Importing from" in captured.out
    assert "tests/assets" in captured.out
    assert "╭─ Python package file structure ─╮" in captured.out
    assert "│  📁 package" in captured.out
    assert "│  ├── 🐍 __init__.py" in captured.out
    assert "│  └── 📁 mod" in captured.out
    assert "│      ├── 🐍 __init__.py " in captured.out
    assert "│      └── 🐍 factory_app.py" in captured.out
    assert "Importing module package.mod.factory_app" in captured.out
    assert "Found importable FastAPI app" in captured.out
    assert "Importable FastAPI app" in captured.out
    assert "from package.mod.factory_app import create_app" in captured.out
    assert "Using import string package.mod.factory_app:create_app" in captured.out


def test_package_factory_api_mod(capsys: CaptureFixture[str]) -> None:
    with changing_dir(assets_path / "package/mod"):
        import_string, is_factory = get_import_string(path=Path("factory_api.py"))
        assert import_string == "package.mod.factory_api:create_api"
        assert is_factory is True

    captured = capsys.readouterr()
    assert "Using path factory_api.py" in captured.out
    assert "Resolved absolute path" in captured.out
    assert "tests/assets/package/mod/factory_api.py" in captured.out
    assert (
        "Searching for package file structure from directories with __init__.py files"
        in captured.out
    )
    assert "Importing from" in captured.out
    assert "tests/assets" in captured.out
    assert "╭─ Python package file structure ─╮" in captured.out
    assert "│  📁 package" in captured.out
    assert "│  ├── 🐍 __init__.py" in captured.out
    assert "│  └── 📁 mod" in captured.out
    assert "│      ├── 🐍 __init__.py " in captured.out
    assert "│      └── 🐍 factory_api.py" in captured.out
    assert "Importing module package.mod.factory_api" in captured.out
    assert "Found importable FastAPI app" in captured.out
    assert "Importable FastAPI app" in captured.out
    assert "from package.mod.factory_api import create_api" in captured.out
    assert "Using import string package.mod.factory_api:create_api" in captured.out


def test_package_factory_other_mod(capsys: CaptureFixture[str]) -> None:
    with changing_dir(assets_path / "package/mod"):
        import_string, is_factory = get_import_string(
            path=Path("factory_other.py"), app_name="build_app"
        )
        assert import_string == "package.mod.factory_other:build_app"
        assert is_factory is True

    captured = capsys.readouterr()
    assert "Using path factory_other.py" in captured.out
    assert "Resolved absolute path" in captured.out
    assert "tests/assets/package/mod/factory_other.py" in captured.out
    assert (
        "Searching for package file structure from directories with __init__.py files"
        in captured.out
    )
    assert "Importing from" in captured.out
    assert "tests/assets" in captured.out
    assert "╭─ Python package file structure ─╮" in captured.out
    assert "│  📁 package" in captured.out
    assert "│  ├── 🐍 __init__.py" in captured.out
    assert "│  └── 📁 mod" in captured.out
    assert "│      ├── 🐍 __init__.py " in captured.out
    assert "│      └── 🐍 factory_other.py" in captured.out
    assert "Importing module package.mod.factory_other" in captured.out
    assert "Found importable FastAPI app" in captured.out
    assert "Importable FastAPI app" in captured.out
    assert "from package.mod.factory_other import build_app" in captured.out
    assert "Using import string package.mod.factory_other:build_app" in captured.out


def test_package_factory_inherit_mod(capsys: CaptureFixture[str]) -> None:
    with changing_dir(assets_path / "package/mod"):
        import_string, is_factory = get_import_string(path=Path("factory_inherit.py"))
        assert import_string == "package.mod.factory_inherit:create_app"
        assert is_factory is True

    captured = capsys.readouterr()
    assert "Using path factory_inherit.py" in captured.out
    assert "Resolved absolute path" in captured.out
    assert "tests/assets/package/mod/factory_inherit.py" in captured.out
    assert (
        "Searching for package file structure from directories with __init__.py files"
        in captured.out
    )
    assert "Importing from" in captured.out
    assert "tests/assets" in captured.out
    assert "╭─ Python package file structure ─╮" in captured.out
    assert "│  📁 package" in captured.out
    assert "│  ├── 🐍 __init__.py" in captured.out
    assert "│  └── 📁 mod" in captured.out
    assert "│      ├── 🐍 __init__.py " in captured.out
    assert "│      └── 🐍 factory_inherit.py" in captured.out
    assert "Importing module package.mod.factory_inherit" in captured.out
    assert "Found importable FastAPI app" in captured.out
    assert "Importable FastAPI app" in captured.out
    assert "from package.mod.factory_inherit import create_app" in captured.out
    assert "Using import string package.mod.factory_inherit:create_app" in captured.out


def test_package_app_parent(capsys: CaptureFixture[str]) -> None:
    with changing_dir(assets_path.parent):
        import_string, is_factory = get_import_string(
            path=Path("assets/package/mod/app.py")
        )
        assert import_string == "package.mod.app:app"
        assert is_factory is False

    captured = capsys.readouterr()
    assert "Using path assets/package/mod/app.py" in captured.out
    assert "Resolved absolute path" in captured.out
    assert "tests/assets/package/mod/app.py" in captured.out
    assert (
        "Searching for package file structure from directories with __init__.py files"
        in captured.out
    )
    assert "Importing from" in captured.out
    assert "tests/assets" in captured.out
    assert "╭─ Python package file structure ─╮" in captured.out
    assert "│  📁 package" in captured.out
    assert "│  ├── 🐍 __init__.py" in captured.out
    assert "│  └── 📁 mod" in captured.out
    assert "│      ├── 🐍 __init__.py " in captured.out
    assert "│      └── 🐍 app.py" in captured.out
    assert "Importing module package.mod.app" in captured.out
    assert "Found importable FastAPI app" in captured.out
    assert "Importable FastAPI app" in captured.out
    assert "from package.mod.app import app" in captured.out
    assert "Using import string package.mod.app:app" in captured.out


def test_package_api_parent(capsys: CaptureFixture[str]) -> None:
    with changing_dir(assets_path.parent):
        import_string, is_factory = get_import_string(
            path=Path("assets/package/mod/api.py")
        )
        assert import_string == "package.mod.api:api"
        assert is_factory is False

    captured = capsys.readouterr()
    assert "Using path assets/package/mod/api.py" in captured.out
    assert "Resolved absolute path" in captured.out
    assert "tests/assets/package/mod/api.py" in captured.out
    assert (
        "Searching for package file structure from directories with __init__.py files"
        in captured.out
    )
    assert "Importing from" in captured.out
    assert "tests/assets" in captured.out
    assert "╭─ Python package file structure ─╮" in captured.out
    assert "│  📁 package" in captured.out
    assert "│  ├── 🐍 __init__.py" in captured.out
    assert "│  └── 📁 mod" in captured.out
    assert "│      ├── 🐍 __init__.py " in captured.out
    assert "│      └── 🐍 api.py" in captured.out
    assert "Importing module package.mod.api" in captured.out
    assert "Found importable FastAPI app" in captured.out
    assert "Importable FastAPI app" in captured.out
    assert "from package.mod.api import api" in captured.out
    assert "Using import string package.mod.api:api" in captured.out


def test_package_other_parent(capsys: CaptureFixture[str]) -> None:
    with changing_dir(assets_path.parent):
        import_string, is_factory = get_import_string(
            path=Path("assets/package/mod/other.py")
        )
        assert import_string == "package.mod.other:first_other"
        assert is_factory is False

    captured = capsys.readouterr()
    assert "Using path assets/package/mod/other.py" in captured.out
    assert "Resolved absolute path" in captured.out
    assert "tests/assets/package/mod/other.py" in captured.out
    assert (
        "Searching for package file structure from directories with __init__.py files"
        in captured.out
    )
    assert "Importing from" in captured.out
    assert "tests/assets" in captured.out
    assert "╭─ Python package file structure ─╮" in captured.out
    assert "│  📁 package" in captured.out
    assert "│  ├── 🐍 __init__.py" in captured.out
    assert "│  └── 📁 mod" in captured.out
    assert "│      ├── 🐍 __init__.py " in captured.out
    assert "│      └── 🐍 other.py" in captured.out
    assert "Importing module package.mod.other" in captured.out
    assert "Found importable FastAPI app" in captured.out
    assert "Importable FastAPI app" in captured.out
    assert "from package.mod.other import first_other" in captured.out
    assert "Using import string package.mod.other:first_other" in captured.out


def test_package_factory_app_parent(capsys: CaptureFixture[str]) -> None:
    with changing_dir(assets_path.parent):
        import_string, is_factory = get_import_string(
            path=Path("assets/package/mod/factory_app.py")
        )
        assert import_string == "package.mod.factory_app:create_app"
        assert is_factory is True

    captured = capsys.readouterr()
    assert "Using path assets/package/mod/factory_app.py" in captured.out
    assert "Resolved absolute path" in captured.out
    assert "tests/assets/package/mod/factory_app.py" in captured.out
    assert (
        "Searching for package file structure from directories with __init__.py files"
        in captured.out
    )
    assert "Importing from" in captured.out
    assert "tests/assets" in captured.out
    assert "╭─ Python package file structure ─╮" in captured.out
    assert "│  📁 package" in captured.out
    assert "│  ├── 🐍 __init__.py" in captured.out
    assert "│  └── 📁 mod" in captured.out
    assert "│      ├── 🐍 __init__.py " in captured.out
    assert "│      └── 🐍 factory_app.py" in captured.out
    assert "Importing module package.mod.factory_app" in captured.out
    assert "Found importable FastAPI app" in captured.out
    assert "Importable FastAPI app" in captured.out
    assert "from package.mod.factory_app import create_app" in captured.out
    assert "Using import string package.mod.factory_app:create_app" in captured.out


def test_package_factory_api_parent(capsys: CaptureFixture[str]) -> None:
    with changing_dir(assets_path.parent):
        import_string, is_factory = get_import_string(
            path=Path("assets/package/mod/factory_api.py")
        )
        assert import_string == "package.mod.factory_api:create_api"
        assert is_factory is True

    captured = capsys.readouterr()
    assert "Using path assets/package/mod/factory_api.py" in captured.out
    assert "Resolved absolute path" in captured.out
    assert "tests/assets/package/mod/factory_api.py" in captured.out
    assert (
        "Searching for package file structure from directories with __init__.py files"
        in captured.out
    )
    assert "Importing from" in captured.out
    assert "tests/assets" in captured.out
    assert "╭─ Python package file structure ─╮" in captured.out
    assert "│  📁 package" in captured.out
    assert "│  ├── 🐍 __init__.py" in captured.out
    assert "│  └── 📁 mod" in captured.out
    assert "│      ├── 🐍 __init__.py " in captured.out
    assert "│      └── 🐍 factory_api.py" in captured.out
    assert "Importing module package.mod.factory_api" in captured.out
    assert "Found importable FastAPI app" in captured.out
    assert "Importable FastAPI app" in captured.out
    assert "from package.mod.factory_api import create_api" in captured.out
    assert "Using import string package.mod.factory_api:create_api" in captured.out


def test_package_factory_other_parent(capsys: CaptureFixture[str]) -> None:
    with changing_dir(assets_path.parent):
        import_string, is_factory = get_import_string(
            path=Path("assets/package/mod/factory_other.py"),
            app_name="build_app",
        )
        assert import_string == "package.mod.factory_other:build_app"
        assert is_factory is True

    captured = capsys.readouterr()
    assert "Using path assets/package/mod/factory_other.py" in captured.out
    assert "Resolved absolute path" in captured.out
    assert "tests/assets/package/mod/factory_other.py" in captured.out
    assert (
        "Searching for package file structure from directories with __init__.py files"
        in captured.out
    )
    assert "Importing from" in captured.out
    assert "tests/assets" in captured.out
    assert "╭─ Python package file structure ─╮" in captured.out
    assert "│  📁 package" in captured.out
    assert "│  ├── 🐍 __init__.py" in captured.out
    assert "│  └── 📁 mod" in captured.out
    assert "│      ├── 🐍 __init__.py " in captured.out
    assert "│      └── 🐍 factory_other.py" in captured.out
    assert "Importing module package.mod.factory_other" in captured.out
    assert "Found importable FastAPI app" in captured.out
    assert "Importable FastAPI app" in captured.out
    assert "from package.mod.factory_other import build_app" in captured.out
    assert "Using import string package.mod.factory_other:build_app" in captured.out


def test_package_factory_inherit_parent(capsys: CaptureFixture[str]) -> None:
    with changing_dir(assets_path.parent):
        import_string, is_factory = get_import_string(
            path=Path("assets/package/mod/factory_inherit.py")
        )
        assert import_string == "package.mod.factory_inherit:create_app"
        assert is_factory is True

    captured = capsys.readouterr()
    assert "Using path assets/package/mod/factory_inherit.py" in captured.out
    assert "Resolved absolute path" in captured.out
    assert "tests/assets/package/mod/factory_inherit.py" in captured.out
    assert (
        "Searching for package file structure from directories with __init__.py files"
        in captured.out
    )
    assert "Importing from" in captured.out
    assert "tests/assets" in captured.out
    assert "╭─ Python package file structure ─╮" in captured.out
    assert "│  📁 package" in captured.out
    assert "│  ├── 🐍 __init__.py" in captured.out
    assert "│  └── 📁 mod" in captured.out
    assert "│      ├── 🐍 __init__.py " in captured.out
    assert "│      └── 🐍 factory_inherit.py" in captured.out
    assert "Importing module package.mod.factory_inherit" in captured.out
    assert "Found importable FastAPI app" in captured.out
    assert "Importable FastAPI app" in captured.out
    assert "from package.mod.factory_inherit import create_app" in captured.out
    assert "Using import string package.mod.factory_inherit:create_app" in captured.out


def test_package_mod_init_inside(capsys: CaptureFixture[str]) -> None:
    with changing_dir(assets_path / "package/mod"):
        import_string, is_factory = get_import_string(path=Path("__init__.py"))
        assert import_string == "package.mod:app"
        assert is_factory is False

    captured = capsys.readouterr()
    assert "Using path __init__.py" in captured.out
    assert "Resolved absolute path" in captured.out
    assert "tests/assets/package/mod/__init__.py" in captured.out
    assert (
        "Searching for package file structure from directories with __init__.py files"
        in captured.out
    )
    assert "Importing from" in captured.out
    assert "tests/assets" in captured.out
    assert "╭─ Python package file structure ─╮" in captured.out
    assert "│  📁 package" in captured.out
    assert "│  ├── 🐍 __init__.py" in captured.out
    assert "│  └── 📁 mod" in captured.out
    assert "│      └── 🐍 __init__.py " in captured.out
    assert "Importing module package.mod" in captured.out
    assert "Found importable FastAPI app" in captured.out
    assert "Importable FastAPI app" in captured.out
    assert "from package.mod import app" in captured.out
    assert "Using import string package.mod:app" in captured.out


def test_package_mod_dir(capsys: CaptureFixture[str]) -> None:
    with changing_dir(assets_path):
        import_string, is_factory = get_import_string(path=Path("package/mod"))
        assert import_string == "package.mod:app"
        assert is_factory is False

    captured = capsys.readouterr()
    assert "Using path package/mod" in captured.out
    assert "Resolved absolute path" in captured.out
    assert "tests/assets/package/mod" in captured.out
    assert (
        "Searching for package file structure from directories with __init__.py files"
        in captured.out
    )
    assert "Importing from" in captured.out
    assert "tests/assets" in captured.out
    assert "╭─ Python package file structure ─╮" in captured.out
    assert "│  📁 package" in captured.out
    assert "│  ├── 🐍 __init__.py" in captured.out
    assert "│  └── 📁 mod" in captured.out
    assert "│      └── 🐍 __init__.py " in captured.out
    assert "Importing module package.mod" in captured.out
    assert "Found importable FastAPI app" in captured.out
    assert "Importable FastAPI app" in captured.out
    assert "from package.mod import app" in captured.out
    assert "Using import string package.mod:app" in captured.out


def test_package_init_inside(capsys: CaptureFixture[str]) -> None:
    with changing_dir(assets_path / "package"):
        import_string, is_factory = get_import_string(path=Path("__init__.py"))
        assert import_string == "package:app"
        assert is_factory is False

    captured = capsys.readouterr()
    assert "Using path __init__.py" in captured.out
    assert "Resolved absolute path" in captured.out
    assert "tests/assets/package/__init__.py" in captured.out
    assert (
        "Searching for package file structure from directories with __init__.py files"
        in captured.out
    )
    assert "Importing from" in captured.out
    assert "tests/assets" in captured.out
    assert "╭─ Python package file structure ─╮" in captured.out
    assert "│  📁 package" in captured.out
    assert "│  └── 🐍 __init__.py" in captured.out
    assert "Importing module package" in captured.out
    assert "Found importable FastAPI app" in captured.out
    assert "Importable FastAPI app" in captured.out
    assert "from package import app" in captured.out
    assert "Using import string package:app" in captured.out


def test_package_dir_inside_package(capsys: CaptureFixture[str]) -> None:
    with changing_dir(assets_path / "package/mod"):
        import_string, is_factory = get_import_string(path=Path("../"))
        assert import_string == "package:app"
        assert is_factory is False

    captured = capsys.readouterr()
    assert "Using path .." in captured.out
    assert "Resolved absolute path" in captured.out
    assert "tests/assets/package" in captured.out
    assert (
        "Searching for package file structure from directories with __init__.py files"
        in captured.out
    )
    assert "Importing from" in captured.out
    assert "tests/assets" in captured.out
    assert "╭─ Python package file structure ─╮" in captured.out
    assert "│  📁 package" in captured.out
    assert "│  └── 🐍 __init__.py" in captured.out
    assert "Importing module package" in captured.out
    assert "Found importable FastAPI app" in captured.out
    assert "Importable FastAPI app" in captured.out
    assert "from package import app" in captured.out
    assert "Using import string package:app" in captured.out


def test_package_dir_above_package(capsys: CaptureFixture[str]) -> None:
    with changing_dir(assets_path.parent):
        import_string, is_factory = get_import_string(path=Path("assets/package"))
        assert import_string == "package:app"
        assert is_factory is False

    captured = capsys.readouterr()
    assert "Using path assets/package" in captured.out
    assert "Resolved absolute path" in captured.out
    assert "tests/assets/package" in captured.out
    assert (
        "Searching for package file structure from directories with __init__.py files"
        in captured.out
    )
    assert "Importing from" in captured.out
    assert "tests/assets" in captured.out
    assert "╭─ Python package file structure ─╮" in captured.out
    assert "│  📁 package" in captured.out
    assert "│  └── 🐍 __init__.py" in captured.out
    assert "Importing module package" in captured.out
    assert "Found importable FastAPI app" in captured.out
    assert "Importable FastAPI app" in captured.out
    assert "from package import app" in captured.out
    assert "Using import string package:app" in captured.out


def test_package_dir_explicit_app(capsys: CaptureFixture[str]) -> None:
    with changing_dir(assets_path):
        import_string, is_factory = get_import_string(
            path=Path("package"), app_name="api"
        )
        assert import_string == "package:api"
        assert is_factory is False

    captured = capsys.readouterr()
    assert "Using path package" in captured.out
    assert "Resolved absolute path" in captured.out
    assert "tests/assets/package" in captured.out
    assert (
        "Searching for package file structure from directories with __init__.py files"
        in captured.out
    )
    assert "Importing from" in captured.out
    assert "tests/assets" in captured.out
    assert "╭─ Python package file structure ─╮" in captured.out
    assert "│  📁 package" in captured.out
    assert "│  └── 🐍 __init__.py" in captured.out
    assert "Importing module package" in captured.out
    assert "Found importable FastAPI app" in captured.out
    assert "Importable FastAPI app" in captured.out
    assert "from package import api" in captured.out
    assert "Using import string package:api" in captured.out


def test_broken_package_dir(capsys: CaptureFixture[str]) -> None:
    with changing_dir(assets_path):
        # TODO (when deprecating Python 3.8): remove ValueError
        with pytest.raises((ImportError, ValueError)):
            get_import_string(path=Path("broken_package/mod/app.py"))

    captured = capsys.readouterr()
    assert "Import error:" in captured.out
    assert "Ensure all the package directories have an __init__.py file" in captured.out


def test_package_dir_no_app() -> None:
    with changing_dir(assets_path):
        with pytest.raises(FastAPICLIException) as e:
            get_import_string(path=Path("package/core/utils.py"))
        assert (
            "Could not find FastAPI app in module, try using --app" in e.value.args[0]
        )


def test_package_dir_object_not_an_app() -> None:
    with changing_dir(assets_path):
        with pytest.raises(FastAPICLIException) as e:
            get_import_string(
                path=Path("package/core/utils.py"), app_name="get_hello_world"
            )
        assert (
            "The app name get_hello_world in package.core.utils doesn't seem to be a FastAPI app"
            in e.value.args[0]
        )


def test_package_dir_object_app_name_not_found() -> None:
    with changing_dir(assets_path):
        with pytest.raises(FastAPICLIException) as e:
            get_import_string(path=Path("package"), app_name="non_existent_app")
        assert "Could not find app name non_existent_app in package" in e.value.args[0]
