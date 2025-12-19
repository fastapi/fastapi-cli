from pathlib import Path
from unittest.mock import patch

import uvicorn
from typer.testing import CliRunner

from fastapi_cli.cli import app
from tests.utils import changing_dir

runner = CliRunner()

assets_path = Path(__file__).parent / "assets"


def test_dev_with_pyproject_app_config_uses() -> None:
    with changing_dir(assets_path / "pyproject_config"), patch.object(
        uvicorn, "run"
    ) as mock_run:
        result = runner.invoke(app, ["dev"])
        assert result.exit_code == 0, result.output

        assert mock_run.call_args.kwargs["app"] == "my_module:app"
        assert mock_run.call_args.kwargs["host"] == "127.0.0.1"
        assert mock_run.call_args.kwargs["port"] == 8000
        assert mock_run.call_args.kwargs["reload"] is True

        assert "Using import string: my_module:app" in result.output


def test_run_with_pyproject_app_config() -> None:
    with changing_dir(assets_path / "pyproject_config"), patch.object(
        uvicorn, "run"
    ) as mock_run:
        result = runner.invoke(app, ["run"])
        assert result.exit_code == 0, result.output

        assert mock_run.call_args.kwargs["app"] == "my_module:app"
        assert mock_run.call_args.kwargs["host"] == "0.0.0.0"
        assert mock_run.call_args.kwargs["port"] == 8000
        assert mock_run.call_args.kwargs["reload"] is False

        assert "Using import string: my_module:app" in result.output


def test_cli_arg_overrides_pyproject_config() -> None:
    with changing_dir(assets_path / "pyproject_config"), patch.object(
        uvicorn, "run"
    ) as mock_run:
        result = runner.invoke(app, ["dev", "another_module.py"])

        assert result.exit_code == 0, result.output

        assert mock_run.call_args.kwargs["app"] == "another_module:app"


def test_pyproject_app_config_invalid_format() -> None:
    test_dir = assets_path / "pyproject_invalid_config"
    test_dir.mkdir(exist_ok=True)

    pyproject_file = test_dir / "pyproject.toml"
    pyproject_file.write_text("""
[tool.fastapi]
entrypoint = "invalid_format_without_colon"
""")

    try:
        with changing_dir(test_dir):
            result = runner.invoke(app, ["dev"])
            assert result.exit_code == 1
            assert (
                "Import string must be in the format module.submodule:app_name"
                in result.output
            )
    finally:
        pyproject_file.unlink()
        test_dir.rmdir()


def test_pyproject_validation_error() -> None:
    test_dir = assets_path / "pyproject_validation_error"
    test_dir.mkdir(exist_ok=True)

    pyproject_file = test_dir / "pyproject.toml"
    pyproject_file.write_text("""
[tool.fastapi]
entrypoint = 123
""")

    try:
        with changing_dir(test_dir):
            result = runner.invoke(app, ["dev"])
            assert result.exit_code == 1
            assert "Invalid configuration in pyproject.toml:" in result.output
            assert "entrypoint" in result.output.lower()
    finally:
        pyproject_file.unlink()
        test_dir.rmdir()
