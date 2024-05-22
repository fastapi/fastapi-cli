import inspect
import sys
from pathlib import Path
from typing import Generator

import pytest
from fastapi_cli.logging import setup_logging
from typer import rich_utils

assets_path = Path(__file__).parent / "assets"


@pytest.fixture(autouse=True)
def reset_syspath() -> Generator[None, None, None]:
    initial_python_path = sys.path.copy()
    try:
        yield
    finally:
        sys.path = initial_python_path


@pytest.fixture(autouse=True, scope="session")
def setup_terminal() -> None:
    rich_utils.MAX_WIDTH = 3000
    rich_utils.FORCE_TERMINAL = False
    setup_logging(terminal_width=3000)
    return


@pytest.fixture(autouse=True)
def asset_import_cleaner() -> Generator[None, None, None]:
    existing_imports = set(sys.modules.keys())
    try:
        yield
    finally:
        # clean up imports
        new_imports = set(sys.modules.keys()) ^ existing_imports
        for name in new_imports:
            try:
                mod_file = inspect.getfile(sys.modules[name])
            except TypeError:  # pragma: no cover
                # builtin, ignore
                pass
            else:
                # only clean up imports from the test directory
                if mod_file.startswith(str(assets_path)):
                    del sys.modules[name]
