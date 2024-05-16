from pathlib import Path

import pytest
from fastapi_cli.discover import get_import_string
from fastapi_cli.exceptions import FastAPICLIException
from pytest import CaptureFixture

from .utils import changing_dir

assets_path = Path(__file__).parent / "assets"


def test_app_dir_main(capsys: CaptureFixture[str]) -> None:
    with changing_dir(assets_path / "default_files" / "default_app_dir_main"):
        import_string = get_import_string()
        assert import_string == "app.main:app"

    captured = capsys.readouterr()
    assert "Using path app/main.py" in captured.out
    assert "Resolved absolute path" in captured.out
    assert (
        "/tests/assets/default_files/default_app_dir_main/app/main.py" in captured.out
    )
    assert "Importing from" in captured.out
    assert "tests/assets/default_files/default_app_dir_main" in captured.out
    assert "╭─ Python package file structure ─╮" in captured.out
    assert "│  📁 app" in captured.out
    assert "│  ├── 🐍 __init__.py" in captured.out
    assert "│  └── 🐍 main.py" in captured.out
    assert "Importing module app.main" in captured.out
    assert "Found importable FastAPI app" in captured.out
    assert "Importable FastAPI app" in captured.out
    assert "from app.main import app" in captured.out
    assert "Using import string app.main:app" in captured.out


def test_app_dir_app(capsys: CaptureFixture[str]) -> None:
    with changing_dir(assets_path / "default_files" / "default_app_dir_app"):
        import_string = get_import_string()
        assert import_string == "app.app:app"

    captured = capsys.readouterr()
    assert "Using path app/app.py" in captured.out
    assert "Resolved absolute path" in captured.out
    assert "/tests/assets/default_files/default_app_dir_app/app/app.py" in captured.out
    assert "Importing from" in captured.out
    assert "tests/assets/default_files/default_app_dir_app" in captured.out
    assert "╭─ Python package file structure ─╮" in captured.out
    assert "│  📁 app" in captured.out
    assert "│  ├── 🐍 __init__.py" in captured.out
    assert "│  └── 🐍 app.py" in captured.out
    assert "Importing module app.app" in captured.out
    assert "Found importable FastAPI app" in captured.out
    assert "Importable FastAPI app" in captured.out
    assert "from app.app import app" in captured.out
    assert "Using import string app.app:app" in captured.out


def test_app_dir_api(capsys: CaptureFixture[str]) -> None:
    with changing_dir(assets_path / "default_files" / "default_app_dir_api"):
        import_string = get_import_string()
        assert import_string == "app.api:app"

    captured = capsys.readouterr()
    assert "Using path app/api.py" in captured.out
    assert "Resolved absolute path" in captured.out
    assert "/tests/assets/default_files/default_app_dir_api/app/api.py" in captured.out
    assert "Importing from" in captured.out
    assert "tests/assets/default_files/default_app_dir_api" in captured.out
    assert "╭─ Python package file structure ─╮" in captured.out
    assert "│  📁 app" in captured.out
    assert "│  ├── 🐍 __init__.py" in captured.out
    assert "│  └── 🐍 api.py" in captured.out
    assert "Importing module app.api" in captured.out
    assert "Found importable FastAPI app" in captured.out
    assert "Importable FastAPI app" in captured.out
    assert "from app.api import app" in captured.out
    assert "Using import string app.api:app" in captured.out


def test_app_dir_non_default() -> None:
    with changing_dir(assets_path / "default_files" / "default_app_dir_non_default"):
        with pytest.raises(FastAPICLIException) as e:
            get_import_string()
        assert (
            "Could not find a default file to run, please provide an explicit path"
            in e.value.args[0]
        )
