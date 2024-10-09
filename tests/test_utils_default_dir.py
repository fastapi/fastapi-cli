from pathlib import Path

import pytest
from fastapi_cli.discover import get_import_string
from fastapi_cli.exceptions import FastAPICLIException
from pytest import CaptureFixture

assets_path = Path(__file__).parent / "assets"


@pytest.mark.parametrize("prog_name", ["app", "api", "main"])
def test_app_dir_main(
    prog_name: str,
    monkeypatch: pytest.MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    monkeypatch.syspath_prepend(
        assets_path / "default_files" / f"default_app_dir_{prog_name}"
    )
    monkeypatch.chdir(assets_path / "default_files" / f"default_app_dir_{prog_name}")

    import_string = get_import_string()
    assert import_string == f"app.{prog_name}:app"

    captured = capsys.readouterr()
    assert f"Using path app/{prog_name}.py" in captured.out
    assert "Resolved absolute path" in captured.out
    assert (
        f"/tests/assets/default_files/default_app_dir_{prog_name}/app/{prog_name}.py"
        in captured.out
    )
    assert "Importing from" in captured.out
    assert f"tests/assets/default_files/default_app_dir_{prog_name}" in captured.out
    assert "╭─ Python package file structure ─╮" in captured.out
    assert "│  📁 app" in captured.out
    assert "│  ├── 🐍 __init__.py" in captured.out
    assert f"│  └── 🐍 {prog_name}.py" in captured.out
    assert f"Importing module app.{prog_name}" in captured.out
    assert "Found importable FastAPI app" in captured.out
    assert "Importable FastAPI app" in captured.out
    assert f"from app.{prog_name} import app" in captured.out
    assert f"Using import string app.{prog_name}:app" in captured.out


def test_app_dir_non_default(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(assets_path / "default_files" / "default_app_dir_non_default")
    with pytest.raises(FastAPICLIException) as e:
        get_import_string()
    assert (
        "Could not find a default file to run, please provide an explicit path"
        in e.value.args[0]
    )
