import logging
import sys
from typing import Union

from rich.console import Console
from rich.logging import RichHandler


def setup_logging(
    terminal_width: Union[int, None] = None, level: int = logging.INFO
) -> None:
    logger = logging.getLogger("fastapi_cli")
    if sys.stdout.isatty():
        # This is a real terminal, use ANSI escape sequences for colored output
        console = Console(width=terminal_width) if terminal_width else None
        rich_handler = RichHandler(
            show_time=False,
            rich_tracebacks=True,
            tracebacks_show_locals=True,
            markup=True,
            show_path=False,
            console=console,
        )
        rich_handler.setFormatter(logging.Formatter("%(message)s"))
        logger.propagate = False
    else:
        # You're being piped or redirected - pass it to the root logger
        pass

    logger.setLevel(level)
