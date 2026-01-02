import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import uvicorn
from typer.testing import CliRunner

from fastapi_cli.cli import app
from fastapi_cli.utils.cli import get_uvicorn_log_config
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
                "reload_dirs": None,
                "workers": None,
                "root_path": "",
                "proxy_headers": True,
                "reload_dirs": None,
                "forwarded_allow_ips": None,
                "log_config": get_uvicorn_log_config(),
            }
        assert "Using import string: single_file_app:app" in result.output
        assert "Starting development server 🚀" in result.output
        assert "Server started at http://127.0.0.1:8000" in result.output
        assert "Documentation at http://127.0.0.1:8000/docs" in result.output
        assert (
            "Running in development mode, for production use: fastapi run"
            in result.output
        )

        assert "🐍 single_file_app.py" in result.output


def test_dev_no_args_auto_discovery() -> None:
    """Test that auto-discovery works when no args and no pyproject.toml entrypoint"""
    with changing_dir(assets_path / "default_files" / "default_main"):
        with patch.object(uvicorn, "run") as mock_run:
            result = runner.invoke(app, ["dev"])  # No path argument
            assert result.exit_code == 0, result.output
            assert mock_run.called
            assert mock_run.call_args
            assert mock_run.call_args.kwargs["app"] == "main:app"
            assert mock_run.call_args.kwargs["host"] == "127.0.0.1"
            assert mock_run.call_args.kwargs["port"] == 8000
            assert mock_run.call_args.kwargs["reload"] is True
        assert "Using import string: main:app" in result.output


def test_dev_package() -> None:
    with changing_dir(assets_path):
        with patch.object(uvicorn, "run") as mock_run:
            result = runner.invoke(app, ["dev", "nested_package/package"])
            assert result.exit_code == 0, result.output
            assert mock_run.called
            assert mock_run.call_args
            assert mock_run.call_args.kwargs == {
                "app": "nested_package.package:app",
                "host": "127.0.0.1",
                "port": 8000,
                "reload": True,
                "reload_dirs": None,
                "workers": None,
                "root_path": "",
                "proxy_headers": True,
                "reload_dirs": None,
                "forwarded_allow_ips": None,
                "log_config": get_uvicorn_log_config(),
            }
        assert "Using import string: nested_package.package:app" in result.output
        assert "Starting development server 🚀" in result.output
        assert "Server started at http://127.0.0.1:8000" in result.output
        assert "Documentation at http://127.0.0.1:8000/docs" in result.output
        assert (
            "Running in development mode, for production use: fastapi run"
            in result.output
        )

        assert "📁 package" in result.output
        assert "└── 🐍 __init__.py" in result.output
        assert "└── 📁 package" in result.output
        assert "    └── 🐍 __init__.py" in result.output


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
                    "--reload-dirs",
                    "api,config",
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
                "reload_dirs": None,
                "workers": None,
                "root_path": "/api",
                "proxy_headers": False,
                "reload_dirs": [
                    "api",
                    "config",
                ],
                "forwarded_allow_ips": None,
                "log_config": get_uvicorn_log_config(),
            }
        assert "Using import string: single_file_app:api" in result.output
        assert "Starting development server 🚀" in result.output
        assert "Server started at http://192.168.0.2:8080" in result.output
        assert "Documentation at http://192.168.0.2:8080/docs" in result.output
        assert (
            "Running in development mode, for production use: fastapi run"
            in result.output
        )


def test_dev_env_vars() -> None:
    with changing_dir(assets_path):
        with patch.object(uvicorn, "run") as mock_run:
            result = runner.invoke(
                app, ["dev", "single_file_app.py"], env={"PORT": "8111"}
            )
            assert result.exit_code == 0, result.output
            assert mock_run.called
            assert mock_run.call_args
            assert mock_run.call_args.kwargs == {
                "app": "single_file_app:app",
                "host": "127.0.0.1",
                "port": 8111,
                "reload": True,
                "reload_dirs": None,
                "workers": None,
                "root_path": "",
                "proxy_headers": True,
                "reload_dirs": None,
                "forwarded_allow_ips": None,
                "log_config": get_uvicorn_log_config(),
            }
        assert "Using import string: single_file_app:app" in result.output
        assert "Starting development server 🚀" in result.output
        assert "Server started at http://127.0.0.1:8111" in result.output
        assert "Documentation at http://127.0.0.1:8111/docs" in result.output
        assert (
            "Running in development mode, for production use: fastapi run"
            in result.output
        )


def test_dev_env_vars_and_args() -> None:
    with changing_dir(assets_path):
        with patch.object(uvicorn, "run") as mock_run:
            result = runner.invoke(
                app,
                [
                    "dev",
                    "single_file_app.py",
                    "--port",
                    "8080",
                ],
                env={"PORT": "8111"},
            )
            assert result.exit_code == 0, result.output
            assert mock_run.called
            assert mock_run.call_args
            assert mock_run.call_args.kwargs == {
                "app": "single_file_app:app",
                "host": "127.0.0.1",
                "port": 8080,
                "reload": True,
                "reload_dirs": None,
                "workers": None,
                "root_path": "",
                "proxy_headers": True,
                "reload_dirs": None,
                "forwarded_allow_ips": None,
                "log_config": get_uvicorn_log_config(),
            }
        assert "Using import string: single_file_app:app" in result.output
        assert "Starting development server 🚀" in result.output
        assert "Server started at http://127.0.0.1:8080" in result.output
        assert "Documentation at http://127.0.0.1:8080/docs" in result.output
        assert (
            "Running in development mode, for production use: fastapi run"
            in result.output
        )


def test_entrypoint_mutually_exclusive_with_path() -> None:
    result = runner.invoke(app, ["dev", "mymodule.py", "--entrypoint", "other:app"])

    assert result.exit_code == 1
    assert (
        "Cannot use --entrypoint together with path or --app arguments" in result.output
    )


def test_entrypoint_mutually_exclusive_with_app() -> None:
    result = runner.invoke(app, ["dev", "--app", "myapp", "--entrypoint", "other:app"])
    assert result.exit_code == 1
    assert (
        "Cannot use --entrypoint together with path or --app arguments" in result.output
    )


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
                "reload_dirs": None,
                "workers": None,
                "root_path": "",
                "proxy_headers": True,
                "reload_dirs": None,
                "forwarded_allow_ips": None,
                "log_config": get_uvicorn_log_config(),
            }
        assert "Using import string: single_file_app:app" in result.output
        assert "Starting production server 🚀" in result.output
        assert "Server started at http://0.0.0.0:8000" in result.output
        assert "Documentation at http://0.0.0.0:8000/docs" in result.output


def test_run_trust_proxy() -> None:
    with changing_dir(assets_path):
        with patch.object(uvicorn, "run") as mock_run:
            result = runner.invoke(
                app, ["run", "single_file_app.py", "--forwarded-allow-ips", "*"]
            )
            assert result.exit_code == 0, result.output
            assert mock_run.called
            assert mock_run.call_args
            assert mock_run.call_args.kwargs == {
                "app": "single_file_app:app",
                "host": "0.0.0.0",
                "port": 8000,
                "reload": False,
                "reload_dirs": None,
                "workers": None,
                "root_path": "",
                "proxy_headers": True,
                "reload_dirs": None,
                "forwarded_allow_ips": "*",
                "log_config": get_uvicorn_log_config(),
            }
        assert "Using import string: single_file_app:app" in result.output
        assert "Starting production server 🚀" in result.output
        assert "Server started at http://0.0.0.0:8000" in result.output
        assert "Documentation at http://0.0.0.0:8000/docs" in result.output
        assert (
            "Running in development mode, for production use: fastapi run"
            not in result.output
        )


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
                "reload_dirs": None,
                "workers": 2,
                "root_path": "/api",
                "proxy_headers": False,
                "reload_dirs": None,
                "forwarded_allow_ips": None,
                "log_config": get_uvicorn_log_config(),
            }

        assert "Using import string: single_file_app:api" in result.output
        assert "Starting production server 🚀" in result.output
        assert "Server started at http://192.168.0.2:8080" in result.output
        assert "Documentation at http://192.168.0.2:8080/docs" in result.output
        assert (
            "Running in development mode, for production use: fastapi run"
            not in result.output
        )


def test_run_env_vars() -> None:
    with changing_dir(assets_path):
        with patch.object(uvicorn, "run") as mock_run:
            result = runner.invoke(
                app, ["run", "single_file_app.py"], env={"PORT": "8111"}
            )
            assert result.exit_code == 0, result.output
            assert mock_run.called
            assert mock_run.call_args
            assert mock_run.call_args.kwargs == {
                "app": "single_file_app:app",
                "host": "0.0.0.0",
                "port": 8111,
                "reload": False,
                "reload_dirs": None,
                "workers": None,
                "root_path": "",
                "proxy_headers": True,
                "reload_dirs": None,
                "forwarded_allow_ips": None,
                "log_config": get_uvicorn_log_config(),
            }
        assert "Using import string: single_file_app:app" in result.output
        assert "Starting production server 🚀" in result.output
        assert "Server started at http://0.0.0.0:8111" in result.output
        assert "Documentation at http://0.0.0.0:8111/docs" in result.output


def test_run_env_vars_and_args() -> None:
    with changing_dir(assets_path):
        with patch.object(uvicorn, "run") as mock_run:
            result = runner.invoke(
                app,
                [
                    "run",
                    "single_file_app.py",
                    "--port",
                    "8080",
                ],
                env={"PORT": "8111"},
            )
            assert result.exit_code == 0, result.output
            assert mock_run.called
            assert mock_run.call_args
            assert mock_run.call_args.kwargs == {
                "app": "single_file_app:app",
                "host": "0.0.0.0",
                "port": 8080,
                "reload": False,
                "reload_dirs": None,
                "workers": None,
                "root_path": "",
                "proxy_headers": True,
                "reload_dirs": None,
                "forwarded_allow_ips": None,
                "log_config": get_uvicorn_log_config(),
            }
        assert "Using import string: single_file_app:app" in result.output
        assert "Starting production server 🚀" in result.output
        assert "Server started at http://0.0.0.0:8080" in result.output
        assert "Documentation at http://0.0.0.0:8080/docs" in result.output


def test_run_error() -> None:
    with changing_dir(assets_path):
        result = runner.invoke(app, ["run", "non_existing_file.py"])
        assert result.exit_code == 1, result.output
        assert "Path does not exist non_existing_file.py" in result.output


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
    assert "Set reload directories explicitly" in result.output
    assert "The root path is used to tell your app" in result.output
    assert "The name of the variable that contains the FastAPI app" in result.output
    assert "Use multiple worker processes." not in result.output
    assert "directories to watch for changes in." in result.output


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
    assert "directories to watch for changes in." not in result.output


def test_callback_help() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0, result.output
    assert "FastAPI CLI - The fastapi command line app." in result.output
    assert "Show the version and exit." in result.output


def test_version() -> None:
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0, result.output
    assert "FastAPI CLI version:" in result.output


def test_dev_reload_dir() -> None:
    with changing_dir(assets_path):
        with patch.object(uvicorn, "run") as mock_run:
            result = runner.invoke(
                app,
                [
                    "dev",
                    "single_file_app.py",
                    "--reload-dir",
                    "src",
                    "--reload-dir",
                    "lib",
                ],
            )
            assert result.exit_code == 0, result.output
            assert mock_run.called
            assert mock_run.call_args
            # Paths are resolved to absolute paths
            reload_dirs = mock_run.call_args.kwargs["reload_dirs"]
            assert len(reload_dirs) == 2
            assert reload_dirs[0] == str((assets_path / "src").resolve())
            assert reload_dirs[1] == str((assets_path / "lib").resolve())


def test_dev_with_import_string() -> None:
    with changing_dir(assets_path):
        with patch.object(uvicorn, "run") as mock_run:
            result = runner.invoke(app, ["dev", "--entrypoint", "single_file_app:api"])
            assert result.exit_code == 0, result.output
            assert mock_run.called
            assert mock_run.call_args
            assert mock_run.call_args.kwargs == {
                "app": "single_file_app:api",
                "forwarded_allow_ips": None,
                "host": "127.0.0.1",
                "port": 8000,
                "reload": True,
                "reload_dirs": None,
                "workers": None,
                "root_path": "",
                "reload_dirs": None,
                "proxy_headers": True,
                "log_config": get_uvicorn_log_config(),
            }
        assert "Using import string: single_file_app:api" in result.output


def test_run_with_import_string() -> None:
    with changing_dir(assets_path):
        with patch.object(uvicorn, "run") as mock_run:
            result = runner.invoke(app, ["run", "--entrypoint", "single_file_app:app"])
            assert result.exit_code == 0, result.output
            assert mock_run.called
            assert mock_run.call_args
            assert mock_run.call_args.kwargs == {
                "app": "single_file_app:app",
                "forwarded_allow_ips": None,
                "host": "0.0.0.0",
                "port": 8000,
                "reload": False,
                "reload_dirs": None,
                "workers": None,
                "root_path": "",
                "reload_dirs": None,
                "proxy_headers": True,
                "log_config": get_uvicorn_log_config(),
            }
        assert "Using import string: single_file_app:app" in result.output


def test_script() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", "-m", "fastapi_cli", "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
