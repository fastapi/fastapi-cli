import sys
from typing import Generator

import pytest
from fastapi_cli.logging import setup_logging
from typer import rich_utils


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
