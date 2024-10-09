from pathlib import Path

import pytest
from fastapi_cli.discover import get_import_string
from fastapi_cli.exceptions import FastAPICLIException
from pytest import CaptureFixture

assets_path = Path(__file__).parent / "assets"


@pytest.mark.parametrize("prog_name", ["api", "app", "main"])
def test_single_file(
    prog_name: str, monkeypatch: pytest.MonkeyPatch, capsys: CaptureFixture[str]
) -> None:
    monkeypatch.chdir(assets_path / "default_files" / f"default_{prog_name}")

    import_string = get_import_string()
    assert import_string == f"{prog_name}:app"

    captured = capsys.readouterr()
    assert f"Using path {prog_name}.py" in captured.out
    assert "Resolved absolute path" in captured.out
    assert (
        f"/tests/assets/default_files/default_{prog_name}/{prog_name}.py"
        in captured.out
    )
    assert "Importing from" in captured.out
    assert f"/tests/assets/default_files/default_{prog_name}" in captured.out
    assert "╭─ Python module file ─╮" in captured.out
    assert f"│  🐍 {prog_name}.py" in captured.out
    assert f"Importing module {prog_name}" in captured.out
    assert "Found importable FastAPI app" in captured.out
    assert "Importable FastAPI app" in captured.out
    assert f"from {prog_name} import app" in captured.out
    assert f"Using import string {prog_name}:app" in captured.out


def test_non_default_file(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(assets_path / "default_files" / "non_default")

    with pytest.raises(FastAPICLIException) as e:
        get_import_string()

    assert (
        "Could not find a default file to run, please provide an explicit path"
        in e.value.args[0]
    )
