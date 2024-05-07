from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Any, Sequence

from click import BadParameter, Context
from typer.core import TyperCommand

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

logger = logging.getLogger(__name__)


def get_toml_key(config: dict[str, Any], keys: Sequence[str]) -> dict[str, Any]:
    for key in keys:
        config = config.get(key, {})
    return config


def read_pyproject_file(keys: Sequence[str]) -> dict[str, Any] | None:
    path = Path("pyproject.toml")
    if not path.exists():
        return None

    with path.open("rb") as f:
        data = tomllib.load(f)

    config = get_toml_key(data, keys)
    return config or None


class CommandWithProjectConfig(TyperCommand):
    """Command class which loads parameters from a pyproject.toml file.

    It will search the current directory and all parent directories for
    a `pyproject.toml` file, then change directories to that file so all paths
    defined in it remain relative to it.

    The table `tool.fastapi.cli` will be used. An additional subtable for the
    running command will also be used. e.g. `tool.fastapi.cli.dev`. Options
    on subcommand tables will override options from the cli table.

    Example:

    ```toml
    [tool.fastapi.cli]
    path = "asgi.py"
    app = "application"

    [tool.fastapi.cli.dev]
    host = "0.0.0.0"
    port = 5000

    [tool.fastapi.cli.run]
    reload = true
    ```
    """

    toml_keys = ("tool", "fastapi", "cli")

    def load_config_table(
        self,
        ctx: Context,
        config: dict[str, Any],
        config_path: str | None = None,
    ) -> None:
        if config_path is not None:
            config = config.get(config_path, {})
        if not config:
            return
        for param in ctx.command.params:
            param_name = param.name or ""
            if param_name in config:
                try:
                    value = param.type_cast_value(ctx, config[param_name])
                except (TypeError, BadParameter) as e:
                    keys: list[str] = list(self.toml_keys)
                    if config_path is not None:
                        keys.append(config_path)
                    keys.append(param_name)
                    full_path = ".".join(keys)
                    ctx.fail(f"Error parsing pyproject.toml: key '{full_path}': {e}")
                else:
                    ctx.params[param_name] = value

    def invoke(self, ctx: Context) -> Any:
        config = read_pyproject_file(self.toml_keys)
        if config is not None:
            logger.info("Loading configuration from pyproject.toml")
            command_name = ctx.command.name or ""
            self.load_config_table(ctx, config)
            self.load_config_table(ctx, config, command_name)

        return super().invoke(ctx)
