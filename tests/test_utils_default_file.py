import importlib
import sys
from pathlib import Path

import pytest
from fastapi_cli.discover import get_import_string
from fastapi_cli.exceptions import FastAPICLIException
from pytest import CaptureFixture

from .utils import changing_dir

assets_path = Path(__file__).parent / "assets"


def test_single_file_main(capsys: CaptureFixture[str]) -> None:
    root_path = assets_path / "default_files" / "default_main"
    old_sys_path = sys.path.copy()
    with changing_dir(root_path):
        sys.path.insert(0, str(root_path))
        mod = importlib.import_module("main")

        importlib.reload(mod)
        import_string = get_import_string()
        assert import_string == "main:app"

    captured = capsys.readouterr()
    assert "Using path main.py" in captured.out
    assert "Resolved absolute path" in captured.out
    assert "/tests/assets/default_files/default_main/main.py" in captured.out
    assert "Importing from" in captured.out
    assert "/tests/assets/default_files/default_main" in captured.out
    assert "╭─ Python module file ─╮" in captured.out
    assert "│  🐍 main.py" in captured.out
    assert "Importing module main" in captured.out
    assert "Found importable FastAPI app" in captured.out
    assert "Importable FastAPI app" in captured.out
    assert "from main import app" in captured.out
    assert "Using import string main:app" in captured.out
    sys.path = old_sys_path


def test_single_file_app(capsys: CaptureFixture[str]) -> None:
    root_path = assets_path / "default_files" / "default_app"
    old_sys_path = sys.path.copy()
    with changing_dir(root_path):
        sys.path.insert(0, str(root_path))
        mod = importlib.import_module("app")

        importlib.reload(mod)
        import_string = get_import_string()
        assert import_string == "app:app"

    captured = capsys.readouterr()
    assert "Using path app.py" in captured.out
    assert "Resolved absolute path" in captured.out
    assert "/tests/assets/default_files/default_app/app.py" in captured.out
    assert "Importing from" in captured.out
    assert "/tests/assets/default_files/default_app" in captured.out
    assert "╭─ Python module file ─╮" in captured.out
    assert "│  🐍 app.py" in captured.out
    assert "Importing module app" in captured.out
    assert "Found importable FastAPI app" in captured.out
    assert "Importable FastAPI app" in captured.out
    assert "from app import app" in captured.out
    assert "Using import string app:app" in captured.out
    sys.path = old_sys_path


def test_single_file_api(capsys: CaptureFixture[str]) -> None:
    root_path = assets_path / "default_files" / "default_api"
    old_sys_path = sys.path.copy()
    with changing_dir(root_path):
        sys.path.insert(0, str(root_path))
        mod = importlib.import_module("api")

        importlib.reload(mod)
        import_string = get_import_string()
        assert import_string == "api:app"

    captured = capsys.readouterr()
    assert "Using path api.py" in captured.out
    assert "Resolved absolute path" in captured.out
    assert "/tests/assets/default_files/default_api/api.py" in captured.out
    assert "Importing from" in captured.out
    assert "/tests/assets/default_files/default_api" in captured.out
    assert "╭─ Python module file ─╮" in captured.out
    assert "│  🐍 api.py" in captured.out
    assert "Importing module api" in captured.out
    assert "Found importable FastAPI app" in captured.out
    assert "Importable FastAPI app" in captured.out
    assert "from api import app" in captured.out
    assert "Using import string api:app" in captured.out
    sys.path = old_sys_path


def test_non_default_file(capsys: CaptureFixture[str]) -> None:
    with changing_dir(assets_path / "default_files" / "non_default"):
        with pytest.raises(FastAPICLIException) as e:
            get_import_string()
        assert (
            "Could not find a default file to run, please provide an explicit path"
            in e.value.args[0]
        )
