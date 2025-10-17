import logging
from pathlib import Path
from typing import Any, Dict, Optional

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class FastAPIConfig(BaseModel):
    entrypoint: Optional[str] = None
    host: str = "127.0.0.1"
    port: int = 8000

    @classmethod
    def _read_pyproject_toml(cls) -> Dict[str, Any]:
        """Read FastAPI configuration from pyproject.toml in current directory."""
        pyproject_path = Path.cwd() / "pyproject.toml"

        if not pyproject_path.exists():
            return {}

        try:
            import tomllib  # type: ignore[import-not-found, unused-ignore]
        except ImportError:
            try:
                import tomli as tomllib  # type: ignore[no-redef, import-not-found, unused-ignore]
            except ImportError:
                logger.debug("tomli not available, skipping pyproject.toml")
                return {}

        with open(pyproject_path, "rb") as f:
            data = tomllib.load(f)

            return data.get("tool", {}).get("fastapi", {})  # type: ignore

    @classmethod
    def resolve(
        cls,
        host: Optional[str] = None,
        port: Optional[int] = None,
        entrypoint: Optional[str] = None,
    ) -> "FastAPIConfig":
        config = cls._read_pyproject_toml()

        if host is not None:
            config["host"] = host
        if port is not None:
            config["port"] = port
        if entrypoint is not None:
            config["entrypoint"] = entrypoint

        return FastAPIConfig.model_validate(config)
