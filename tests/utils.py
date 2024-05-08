from __future__ import annotations

import os
import sys
import warnings
from contextlib import contextmanager
from pathlib import Path
from typing import Generator, Union


@contextmanager
def changing_dir(directory: Union[str, Path]) -> Generator[None, None, None]:
    initial_dir = os.getcwd()
    os.chdir(directory)
    try:
        yield
    finally:
        os.chdir(initial_dir)


@contextmanager
def importing(names: list[str]) -> Generator[None, None, None]:
    for name in names:
        if name in sys.modules:  # pragma: no cover
            warnings.warn(
                f"{name} is already imported",
                category=UserWarning,
                stacklevel=1,
            )
    try:
        yield
    finally:
        for name in names:
            if name in sys.modules:
                del sys.modules[name]
