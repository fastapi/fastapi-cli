from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Any
from unittest.mock import patch

import pytest
import uvicorn
from fastapi_cli.cli import app
from typer.testing import CliRunner

from tests.utils import changing_dir

runner = CliRunner()

assets_path = Path(__file__).parent / "assets"


def test_dev() -> None:
    with changing_dir(assets_path):
        with patch.object(uvicorn, "run") as mock_run:
            result = runner.invoke(app, ["dev", "single_file_app.py"])
            assert result.exit_code == 0, result.output
            assert mock_run.called
            assert mock_run.call_args
            assert mock_run.call_args.kwargs == {
                "app": "single_file_app:app",
                "host": "127.0.0.1",
                "port": 8000,
                "reload": True,
                "workers": None,
                "root_path": "",
                "proxy_headers": True,
            }
        assert "Using import string single_file_app:app" in result.output
        assert (
            "╭────────── FastAPI CLI - Development mode ───────────╮" in result.output
        )
        assert "│  Serving at: http://127.0.0.1:8000" in result.output
        assert "│  API docs: http://127.0.0.1:8000/docs" in result.output
        assert "│  Running in development mode, for production use:" in result.output
        assert "│  fastapi run" in result.output


def test_dev_args() -> None:
    with changing_dir(assets_path):
        with patch.object(uvicorn, "run") as mock_run:
            result = runner.invoke(
                app,
                [
                    "dev",
                    "single_file_app.py",
                    "--host",
                    "192.168.0.2",
                    "--port",
                    "8080",
                    "--no-reload",
                    "--root-path",
                    "/api",
                    "--app",
                    "api",
                    "--no-proxy-headers",
                ],
            )
            assert result.exit_code == 0, result.output
            assert mock_run.called
            assert mock_run.call_args
            assert mock_run.call_args.kwargs == {
                "app": "single_file_app:api",
                "host": "192.168.0.2",
                "port": 8080,
                "reload": False,
                "workers": None,
                "root_path": "/api",
                "proxy_headers": False,
            }
        assert "Using import string single_file_app:api" in result.output
        assert (
            "╭────────── FastAPI CLI - Development mode ───────────╮" in result.output
        )
        assert "│  Serving at: http://192.168.0.2:8080" in result.output
        assert "│  API docs: http://192.168.0.2:8080/docs" in result.output
        assert "│  Running in development mode, for production use:" in result.output
        assert "│  fastapi run" in result.output


def test_project_run() -> None:
    with changing_dir(assets_path / "projects/configured_app"):
        with patch.object(uvicorn, "run") as mock_run:
            result = runner.invoke(app, ["run"])
            assert result.exit_code == 0, result.output
            assert mock_run.called
            assert mock_run.call_args
            assert mock_run.call_args.kwargs == {
                "app": "server:application",
                "host": "0.0.0.0",
                "port": 8000,
                "reload": False,
                "workers": None,
                "root_path": "",
                "proxy_headers": True,
            }


@pytest.mark.parametrize(
    ("command", "kwargs"),
    [
        ("run", {"host": "0.0.0.0", "port": 8001, "workers": 4}),
        ("dev", {"host": "127.0.0.1", "port": 8002, "workers": None}),
    ],
)
def test_project_run_subconfigure(command: str, kwargs: dict[str, Any]) -> None:
    with changing_dir(assets_path / "projects/configured_app_subtable"):
        with patch.object(uvicorn, "run") as mock_run:
            result = runner.invoke(app, [command])
            assert result.exit_code == 0, result.output
            assert mock_run.called
            assert mock_run.call_args
            assert mock_run.call_args.kwargs == {
                "app": "app:app",
                "reload": True,
                "root_path": "",
                "proxy_headers": True,
                **kwargs,
            }


def test_run() -> None:
    with changing_dir(assets_path):
        with patch.object(uvicorn, "run") as mock_run:
            result = runner.invoke(app, ["run", "single_file_app.py"])
            assert result.exit_code == 0, result.output
            assert mock_run.called
            assert mock_run.call_args
            assert mock_run.call_args.kwargs == {
                "app": "single_file_app:app",
                "host": "0.0.0.0",
                "port": 8000,
                "reload": False,
                "workers": None,
                "root_path": "",
                "proxy_headers": True,
            }
        assert "Using import string single_file_app:app" in result.output
        assert (
            "╭─────────── FastAPI CLI - Production mode ───────────╮" in result.output
        )
        assert "│  Serving at: http://0.0.0.0:8000" in result.output
        assert "│  API docs: http://0.0.0.0:8000/docs" in result.output
        assert "│  Running in production mode, for development use:" in result.output
        assert "│  fastapi dev" in result.output


def test_run_args() -> None:
    with changing_dir(assets_path):
        with patch.object(uvicorn, "run") as mock_run:
            result = runner.invoke(
                app,
                [
                    "run",
                    "single_file_app.py",
                    "--host",
                    "192.168.0.2",
                    "--port",
                    "8080",
                    "--no-reload",
                    "--workers",
                    "2",
                    "--root-path",
                    "/api",
                    "--app",
                    "api",
                    "--no-proxy-headers",
                ],
            )
            assert result.exit_code == 0, result.output
            assert mock_run.called
            assert mock_run.call_args
            assert mock_run.call_args.kwargs == {
                "app": "single_file_app:api",
                "host": "192.168.0.2",
                "port": 8080,
                "reload": False,
                "workers": 2,
                "root_path": "/api",
                "proxy_headers": False,
            }
        assert "Using import string single_file_app:api" in result.output
        assert (
            "╭─────────── FastAPI CLI - Production mode ───────────╮" in result.output
        )
        assert "│  Serving at: http://192.168.0.2:8080" in result.output
        assert "│  API docs: http://192.168.0.2:8080/docs" in result.output
        assert "│  Running in production mode, for development use:" in result.output
        assert "│  fastapi dev" in result.output


def test_run_error() -> None:
    with changing_dir(assets_path):
        result = runner.invoke(app, ["run", "non_existing_file.py"])
        assert result.exit_code == 1, result.output
        assert "Path does not exist non_existing_file.py" in result.output


def test_project_config_error() -> None:
    with changing_dir(assets_path / "projects/bad_configured_app"):
        result = runner.invoke(app, ["run"])
        assert result.exit_code == 2, result.output
        assert (
            "Error parsing pyproject.toml: key 'tool.fastapi.cli.run.port'"
            in result.output
        )


def test_dev_help() -> None:
    result = runner.invoke(app, ["dev", "--help"])
    assert result.exit_code == 0, result.output
    assert "Run a FastAPI app in development mode." in result.output
    assert (
        "This is equivalent to fastapi run but with reload enabled and listening on the 127.0.0.1 address."
        in result.output
    )
    assert (
        "Otherwise, it uses the first FastAPI app found in the imported module or package."
        in result.output
    )
    assert "A path to a Python file or package directory" in result.output
    assert "The host to serve on." in result.output
    assert "The port to serve on." in result.output
    assert "Enable auto-reload of the server when (code) files change." in result.output
    assert "The root path is used to tell your app" in result.output
    assert "The name of the variable that contains the FastAPI app" in result.output
    assert "Use multiple worker processes." not in result.output


def test_run_help() -> None:
    result = runner.invoke(app, ["run", "--help"])
    assert result.exit_code == 0, result.output
    assert "Run a FastAPI app in production mode." in result.output
    assert (
        "This is equivalent to fastapi dev but with reload disabled and listening on the 0.0.0.0 address."
        in result.output
    )
    assert (
        "Otherwise, it uses the first FastAPI app found in the imported module or package."
        in result.output
    )
    assert "A path to a Python file or package directory" in result.output
    assert "The host to serve on." in result.output
    assert "The port to serve on." in result.output
    assert "Enable auto-reload of the server when (code) files change." in result.output
    assert "The root path is used to tell your app" in result.output
    assert "The name of the variable that contains the FastAPI app" in result.output
    assert "Use multiple worker processes." in result.output


def test_callback_help() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0, result.output
    assert "FastAPI CLI - The fastapi command line app." in result.output
    assert "Show the version and exit." in result.output


def test_version() -> None:
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0, result.output
    assert "FastAPI CLI version:" in result.output


def test_script() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", "-m", "fastapi_cli", "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
