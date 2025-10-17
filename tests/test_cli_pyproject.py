from pathlib import Path
from unittest.mock import patch

import uvicorn
from typer.testing import CliRunner

from fastapi_cli.cli import app
from fastapi_cli.utils.cli import get_uvicorn_log_config
from tests.utils import changing_dir

runner = CliRunner()

assets_path = Path(__file__).parent / "assets"


def test_dev_with_pyproject_app_config() -> None:
    with changing_dir(assets_path / "pyproject_config"), patch.object(
        uvicorn, "run"
    ) as mock_run:
        result = runner.invoke(app, ["dev"])
        assert result.exit_code == 0, result.output
        assert mock_run.called
        assert mock_run.call_args
        assert mock_run.call_args.kwargs == {
            "app": "mymodule:app",
            "host": "127.0.0.1",
            "port": 8000,
            "reload": True,
            "workers": None,
            "root_path": "",
            "proxy_headers": True,
            "forwarded_allow_ips": None,
            "log_config": get_uvicorn_log_config(),
        }
        assert "Using import string: mymodule:app" in result.output


def test_run_with_pyproject_app_config() -> None:
    with changing_dir(assets_path / "pyproject_config"), patch.object(
        uvicorn, "run"
    ) as mock_run:
        result = runner.invoke(app, ["run"])
        assert result.exit_code == 0, result.output
        assert mock_run.called
        assert mock_run.call_args
        assert mock_run.call_args.kwargs["app"] == "mymodule:app"
        assert mock_run.call_args.kwargs["host"] == "0.0.0.0"
        assert mock_run.call_args.kwargs["port"] == 8000
        assert mock_run.call_args.kwargs["reload"] is False


def test_cli_arg_overrides_pyproject_config() -> None:
    """Test that CLI arguments override pyproject.toml configuration"""
    with changing_dir(assets_path / "pyproject_config"):
        # Create another file to test override
        other_app = assets_path / "pyproject_config" / "other.py"
        other_app.write_text("""
from fastapi import FastAPI

api = FastAPI()

@api.get("/")
def read_root():
    return {"source": "other"}
""")

        try:
            with patch.object(uvicorn, "run") as mock_run:
                result = runner.invoke(app, ["dev", "other.py", "--app", "api"])
                assert result.exit_code == 0, result.output
                assert mock_run.called
                assert mock_run.call_args
                assert mock_run.call_args.kwargs["app"] == "other:api"
        finally:
            other_app.unlink()


def test_pyproject_app_config_invalid_format() -> None:
    """Test error handling for invalid app format in pyproject.toml"""

    # Create a test directory with invalid config
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


def test_dev_without_pyproject_toml() -> None:
    """Test that dev command works without pyproject.toml file"""
    # Use an existing test directory that has a main.py but no pyproject.toml
    test_dir = assets_path / "default_files" / "default_main"

    with changing_dir(test_dir):
        with patch.object(uvicorn, "run") as mock_run:
            result = runner.invoke(app, ["dev"])
            assert result.exit_code == 0, result.output
            assert mock_run.called
            assert mock_run.call_args
            # Should use defaults since no config file
            assert mock_run.call_args.kwargs["host"] == "127.0.0.1"
            assert mock_run.call_args.kwargs["port"] == 8000
            assert mock_run.call_args.kwargs["app"] == "main:app"


def test_pyproject_validation_error() -> None:
    """Test error handling for validation errors in pyproject.toml"""
    # Create a test directory with invalid config (invalid entrypoint type)
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


def test_entrypoint_mutually_exclusive_with_path() -> None:
    """Test that --entrypoint cannot be used with path argument"""
    with changing_dir(assets_path / "pyproject_config"):
        result = runner.invoke(app, ["dev", "mymodule.py", "--entrypoint", "other:app"])
        assert result.exit_code == 1
        assert (
            "Cannot use --entrypoint together with path or --app arguments"
            in result.output
        )


def test_entrypoint_mutually_exclusive_with_app() -> None:
    """Test that --entrypoint cannot be used with --app flag"""
    with changing_dir(assets_path / "pyproject_config"):
        result = runner.invoke(app, ["dev", "--app", "myapp", "--entrypoint", "other:app"])
        assert result.exit_code == 1
        assert (
            "Cannot use --entrypoint together with path or --app arguments"
            in result.output
        )
