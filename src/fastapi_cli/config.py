import logging
from pathlib import Path
from typing import Any

from pydantic import BaseModel, StrictStr

from fastapi_cli.exceptions import FastAPICLIException

logger = logging.getLogger(__name__)


class FastAPIConfig(BaseModel):
    entrypoint: StrictStr | None = None
    from_pyproject: bool = False

    @classmethod
    def _read_pyproject_toml(cls) -> dict[str, Any]:
        """Read FastAPI configuration from pyproject.toml in current directory."""
        pyproject_path = Path.cwd() / "pyproject.toml"

        if not pyproject_path.exists():
            return {}

        try:
            import tomllib  # type: ignore[import-not-found, unused-ignore]  # ty: ignore[unresolved-import]
        except ImportError:
            try:
                import tomli as tomllib  # type: ignore[no-redef, import-not-found, unused-ignore]
            except ImportError:  # pragma: no cover
                logger.debug("tomli not available, skipping pyproject.toml")
                return {}

        with open(pyproject_path, "rb") as f:
            try:
                data = tomllib.load(f)
            except tomllib.TOMLDecodeError as e:
                raise FastAPICLIException(f"Invalid TOML in pyproject.toml: {e}") from e

            return data.get("tool", {}).get("fastapi", {})  # type: ignore[no-any-return]

    @classmethod
    def resolve(cls, entrypoint: str | None = None) -> "FastAPIConfig":
        config = cls._read_pyproject_toml()

        if entrypoint is not None:
            config["entrypoint"] = entrypoint

        config["from_pyproject"] = ("entrypoint" in config) and (entrypoint is None)

        return cls.model_validate(config)
