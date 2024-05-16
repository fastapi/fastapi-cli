from pathlib import Path

import pytest
from fastapi_cli.discover import get_import_string
from fastapi_cli.exceptions import FastAPICLIException
from pytest import CaptureFixture

from .utils import changing_dir

assets_path = Path(__file__).parent / "assets"


def test_single_file_app(capsys: CaptureFixture[str]) -> None:
    with changing_dir(assets_path):
        import_string = get_import_string(path=Path("single_file_app.py"))
        assert import_string == "single_file_app:app"

    captured = capsys.readouterr()
    assert "Using path single_file_app.py" in captured.out
    assert "Resolved absolute path" in captured.out
    assert "/tests/assets/single_file_app.py" in captured.out
    assert (
        "Searching for package file structure from directories with __init__.py files"
        in captured.out
    )
    assert "Importing from" in captured.out
    assert "tests/assets" in captured.out
    assert "╭── Python module file ───╮" in captured.out
    assert "│  🐍 single_file_app.py" in captured.out
    assert "Importing module single_file_app" in captured.out
    assert "Found importable FastAPI app" in captured.out
    assert "Importable FastAPI app" in captured.out
    assert "from single_file_app import app" in captured.out
    assert "Using import string single_file_app:app" in captured.out


def test_single_file_api(capsys: CaptureFixture[str]) -> None:
    with changing_dir(assets_path):
        import_string = get_import_string(path=Path("single_file_api.py"))
        assert import_string == "single_file_api:api"

    captured = capsys.readouterr()
    assert "Using path single_file_api.py" in captured.out
    assert "Resolved absolute path" in captured.out
    assert "tests/assets/single_file_api.py" in captured.out
    assert (
        "Searching for package file structure from directories with __init__.py files"
        in captured.out
    )
    assert "Importing from" in captured.out
    assert "tests/assets" in captured.out
    assert "╭── Python module file ───╮" in captured.out
    assert "│  🐍 single_file_api.py" in captured.out
    assert "Importing module single_file_api" in captured.out
    assert "Found importable FastAPI app" in captured.out
    assert "Importable FastAPI app" in captured.out
    assert "from single_file_api import api" in captured.out
    assert "Using import string single_file_api:api" in captured.out


def test_single_file_other(capsys: CaptureFixture[str]) -> None:
    with changing_dir(assets_path):
        import_string = get_import_string(path=Path("single_file_other.py"))
        assert import_string == "single_file_other:first_other"

    captured = capsys.readouterr()
    assert "Using path single_file_other.py" in captured.out
    assert "Resolved absolute path" in captured.out
    assert "tests/assets/single_file_other.py" in captured.out
    assert (
        "Searching for package file structure from directories with __init__.py files"
        in captured.out
    )
    assert "Importing from" in captured.out
    assert "tests/assets" in captured.out
    assert "╭─── Python module file ────╮" in captured.out
    assert "│  🐍 single_file_other.py" in captured.out
    assert "Importing module single_file_other" in captured.out
    assert "Found importable FastAPI app" in captured.out
    assert "Importable FastAPI app" in captured.out
    assert "from single_file_other import first_other" in captured.out
    assert "Using import string single_file_other:first_other" in captured.out


def test_single_file_explicit_object(capsys: CaptureFixture[str]) -> None:
    with changing_dir(assets_path):
        import_string = get_import_string(
            path=Path("single_file_app.py"), app_name="second_other"
        )
        assert import_string == "single_file_app:second_other"

    captured = capsys.readouterr()
    assert "Using path single_file_app.py" in captured.out
    assert "Resolved absolute path" in captured.out
    assert "tests/assets/single_file_app.py" in captured.out
    assert (
        "Searching for package file structure from directories with __init__.py files"
        in captured.out
    )
    assert "Importing from" in captured.out
    assert "tests/assets" in captured.out
    assert "╭── Python module file ───╮" in captured.out
    assert "│  🐍 single_file_app.py" in captured.out
    assert "Importing module single_file_app" in captured.out
    assert "Found importable FastAPI app" in captured.out
    assert "Importable FastAPI app" in captured.out
    assert "from single_file_app import second_other" in captured.out
    assert "Using import string single_file_app:second_other" in captured.out


def test_single_non_existing_file() -> None:
    with changing_dir(assets_path):
        with pytest.raises(FastAPICLIException) as e:
            get_import_string(path=assets_path / "non_existing.py")
    assert "Path does not exist" in e.value.args[0]
