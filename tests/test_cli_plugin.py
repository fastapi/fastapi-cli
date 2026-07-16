import sys
from collections.abc import Generator
from importlib.metadata import EntryPoint
from pathlib import Path
from unittest.mock import patch

import pytest
import typer

from fastapi_cli.cli import _load_cli_plugins

assets_path = Path(__file__).parent / "assets"


@pytest.fixture
def plugins_on_path() -> Generator[None, None, None]:
    original_path = sys.path.copy()
    sys.path.insert(0, str(assets_path))
    try:
        yield
    finally:
        sys.path[:] = original_path
        for key in list(sys.modules.keys()):
            if key.startswith("plugins."):
                del sys.modules[key]


@pytest.fixture
def app() -> typer.Typer:
    app = typer.Typer()
    return app


def _entry_point(name: str, module_attr: str) -> EntryPoint:
    return EntryPoint(
        name=name,
        value=f"plugins.{module_attr}",
        group="fastapi_cli.plugins",
    )


def test_load_cli_plugins_happy_path(
    plugins_on_path: None,
    app: typer.Typer,
) -> None:
    entry_point = _entry_point("sample", "sample:register")

    with patch("fastapi_cli.cli._entry_points", return_value=[entry_point]):
        _load_cli_plugins(app)

    names = {registered_command.name for registered_command in app.registered_commands}
    assert "ping" in names


def test_load_cli_plugins_logs_on_failure(
    plugins_on_path: None,
    app: typer.Typer,
) -> None:
    entry_point = _entry_point("broken", "broken:register")

    with (
        patch("fastapi_cli.cli._entry_points", return_value=[entry_point]),
        patch("fastapi_cli.cli.logger") as mock_logger,
    ):
        _load_cli_plugins(app)

    mock_logger.warning.assert_called_once()
    _fmt, entry_point_name, *_ = mock_logger.warning.call_args.args
    assert entry_point_name == "broken"


def test_load_cli_plugins_warns_on_collision_with_builtin(
    plugins_on_path: None,
    app: typer.Typer,
) -> None:

    @app.command("dev")
    def existing() -> None:
        pass  # pragma: no cover

    entry_point = _entry_point("colliding", "colliding:register")

    with (
        patch("fastapi_cli.cli._entry_points", return_value=[entry_point]),
        patch("fastapi_cli.cli.logger") as mock_logger,
    ):
        _load_cli_plugins(app)

    mock_logger.warning.assert_called_once()
    _fmt, entry_point_name, collisions = mock_logger.warning.call_args.args
    assert entry_point_name == "colliding"
    assert "dev" in collisions


def test_load_cli_plugins_warns_on_cross_plugin_collision(
    plugins_on_path: None,
    app: typer.Typer,
) -> None:
    first = _entry_point("sample", "sample:register")
    duplicate = _entry_point("duplicate", "sample:register")

    with (
        patch("fastapi_cli.cli._entry_points", return_value=[first, duplicate]),
        patch("fastapi_cli.cli.logger") as mock_logger,
    ):
        _load_cli_plugins(app)

    mock_logger.warning.assert_called_once()
    _fmt, entry_point_name, collisions = mock_logger.warning.call_args.args
    assert entry_point_name == "duplicate"
    assert "ping" in collisions
