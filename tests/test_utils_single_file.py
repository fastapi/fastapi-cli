from pathlib import Path
from typing import Optional

import pytest
from fastapi_cli.discover import get_import_string
from fastapi_cli.exceptions import FastAPICLIException
from pytest import CaptureFixture

assets_path = Path(__file__).parent / "assets"


@pytest.fixture(autouse=True)
def chdir_assets(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(assets_path)


@pytest.mark.parametrize(
    ("module_name", "app_name", "import_name"),
    [
        ("app", "app", None),
        ("api", "api", None),
        ("other", "first_other", None),
        ("other", "second_other", "second_other"),
    ],
)
def test_single_file_app(
    module_name: str,
    app_name: str,
    import_name: Optional[str],
    capsys: CaptureFixture[str],
) -> None:
    import_string = get_import_string(
        path=Path(f"single_file_{module_name}.py"), app_name=import_name
    )
    assert import_string == f"single_file_{module_name}:{app_name}"

    captured = capsys.readouterr()
    assert f"Using path single_file_{module_name}.py" in captured.out
    assert "Resolved absolute path" in captured.out
    assert f"/tests/assets/single_file_{module_name}.py" in captured.out
    assert (
        "Searching for package file structure from directories with __init__.py files"
        in captured.out
    )
    assert "Importing from" in captured.out
    assert "tests/assets" in captured.out
    assert (
        "╭─── Python module file ────╮" in captured.out
        or "╭── Python module file ───╮" in captured.out
    )

    assert f"│  🐍 single_file_{module_name}.py" in captured.out
    assert f"Importing module single_file_{module_name}" in captured.out
    assert "Found importable FastAPI app" in captured.out
    assert "Importable FastAPI app" in captured.out
    assert f"from single_file_{module_name} import {app_name}" in captured.out
    assert f"Using import string single_file_{module_name}:{app_name}" in captured.out


def test_single_non_existing_file() -> None:
    with pytest.raises(FastAPICLIException) as e:
        get_import_string(path=assets_path / "non_existing.py")
    assert "Path does not exist" in e.value.args[0]
