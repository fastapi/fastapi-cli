from pathlib import Path

import pytest
from fastapi_cli.discover import get_import_string
from fastapi_cli.exceptions import FastAPICLIException
from typer.testing import CliRunner

runner = CliRunner()

assets_path = Path(__file__).parent / "assets"


def test_no_uvicorn(monkeypatch: pytest.MonkeyPatch) -> None:
    import fastapi_cli.cli

    monkeypatch.setattr(fastapi_cli.cli, "uvicorn", None)
    monkeypatch.chdir(assets_path)
    result = runner.invoke(fastapi_cli.cli.app, ["dev", "single_file_app.py"])
    assert result.exit_code == 1
    assert result.exception is not None
    assert (
        "Could not import Uvicorn, try running 'pip install uvicorn'"
        in result.exception.args[0]
    )


def test_no_fastapi(monkeypatch: pytest.MonkeyPatch) -> None:
    import fastapi_cli.discover

    monkeypatch.setattr(fastapi_cli.discover, "FastAPI", None)
    monkeypatch.chdir(assets_path)

    with pytest.raises(FastAPICLIException) as exc_info:
        get_import_string(path=Path("single_file_app.py"))
    assert "Could not import FastAPI, try running 'pip install fastapi'" in str(
        exc_info.value
    )
