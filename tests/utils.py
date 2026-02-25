import os
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path
from typing import Union


@contextmanager
def changing_dir(directory: Union[str, Path]) -> Generator[None, None, None]:
    initial_dir = os.getcwd()
    os.chdir(directory)
    try:
        yield
    finally:
        os.chdir(initial_dir)
