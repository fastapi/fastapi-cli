import logging
from pathlib import Path
from typing import Any, Dict, Optional

from pydantic import BaseModel, StrictStr
from pydantic.version import VERSION as PYDANTIC_VERSION

logger = logging.getLogger(__name__)

PYDANTIC_VERSION_MINOR_TUPLE = tuple(int(x) for x in PYDANTIC_VERSION.split(".")[:2])
PYDANTIC_V2 = PYDANTIC_VERSION_MINOR_TUPLE[0] == 2


class FastAPIConfig(BaseModel):
    entrypoint: Optional[StrictStr] = None

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
            except ImportError:  # pragma: no cover
                logger.debug("tomli not available, skipping pyproject.toml")
                return {}

        with open(pyproject_path, "rb") as f:
            data = tomllib.load(f)

            return data.get("tool", {}).get("fastapi", {})  # type: ignore

    @classmethod
    def resolve(cls, entrypoint: Optional[str] = None) -> "FastAPIConfig":
        config = cls._read_pyproject_toml()

        if entrypoint is not None:
            config["entrypoint"] = entrypoint

        # Pydantic v2 uses model_validate, v1 uses parse_obj
        if not PYDANTIC_V2:
            return cls.parse_obj(config)  # type: ignore[no-any-return, unused-ignore]

        return cls.model_validate(config)  # type: ignore[no-any-return, unused-ignore, attr-defined]
