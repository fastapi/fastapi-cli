import os
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path


@contextmanager
def changing_dir(directory: str | Path) -> Generator[None, None, None]:
    initial_dir = os.getcwd()
    os.chdir(directory)
    try:
        yield
    finally:
        os.chdir(initial_dir)
