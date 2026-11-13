import tomllib
from pathlib import Path
from typing import Any

from pydantic import BaseModel, StrictStr


class FastAPIConfig(BaseModel):
    entrypoint: StrictStr | None = None
    from_pyproject: bool = False

    @classmethod
    def _read_pyproject_toml(cls) -> dict[str, Any]:
        """Read FastAPI configuration from pyproject.toml in current directory."""
        pyproject_path = Path.cwd() / "pyproject.toml"

        if not pyproject_path.exists():
            return {}

        with open(pyproject_path, "rb") as f:
            data = tomllib.load(f)

            return data.get("tool", {}).get("fastapi", {})  # type: ignore[no-any-return]

    @classmethod
    def resolve(cls, entrypoint: str | None = None) -> "FastAPIConfig":
        config = cls._read_pyproject_toml()

        if entrypoint is not None:
            config["entrypoint"] = entrypoint

        config["from_pyproject"] = ("entrypoint" in config) and (entrypoint is None)

        return cls.model_validate(config)
