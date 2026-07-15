import logging
import sys
from typing import Any

from rich._loop import loop_first
from rich.console import Console, ConsoleOptions, RenderableType, RenderResult
from rich.segment import Segment
from rich.text import Text
from rich_toolkit import RichToolkit
from rich_toolkit.element import Element
from rich_toolkit.styles import BaseStyle
from uvicorn.logging import DefaultFormatter

logger = logging.getLogger(__name__)


def should_use_rich_logs() -> bool:
    """Return True when stdout is a TTY and rich logs should be used, False otherwise."""
    return sys.stdout.isatty()


class IndentedBlock:
    """Indent a renderable, hanging a prefix (e.g. an emoji bullet) on the
    first line and aligning wrapped/extra lines under the text."""

    def __init__(
        self,
        renderable: RenderableType,
        *,
        first_prefix: Text,
        prefix: Text,
    ) -> None:
        self.renderable = renderable
        self.first_prefix = first_prefix
        self.prefix = prefix

        # Text renders its `end` ("\n" by default), which would break lines
        self.first_prefix.end = ""
        self.prefix.end = ""

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        prefix_width = max(self.first_prefix.cell_len, self.prefix.cell_len)
        lines = console.render_lines(
            self.renderable,
            options.update_width(options.max_width - prefix_width),
            pad=False,
        )

        new_line = Segment.line()

        for first, line in loop_first(lines):
            if any(segment.text.strip() for segment in line):
                yield from console.render(
                    self.first_prefix if first else self.prefix, options
                )
                yield from line

            yield new_line


class FastAPIStyle(BaseStyle):
    """Uniform left indent with emoji bullets hanging to the left of the text.

    ``emoji=`` renders as a bullet in a fixed column; ``bullet=False`` drops
    the bullet column and just indents. This is a small, purpose-built subset
    of the richer style in fastapi-cloud-cli.
    """

    content_padding = 1
    emoji_column_width = 3

    def render_element(
        self,
        element: Any,
        is_active: bool = False,
        done: bool = False,
        parent: Element | None = None,
        **kwargs: Any,
    ) -> RenderableType:
        rendered = super().render_element(
            element=element, is_active=is_active, done=done, parent=parent, **kwargs
        )

        emoji = kwargs.get("emoji", "")

        if not emoji and not kwargs.get("bullet", True):
            indent = Text(" " * (self.content_padding + 1))
            return IndentedBlock(rendered, first_prefix=indent, prefix=indent)

        return IndentedBlock(
            rendered,
            first_prefix=self._get_bullet_prefix(emoji),
            prefix=Text(" " * (self.content_padding + self.emoji_column_width)),
        )

    def _get_bullet_prefix(self, emoji: str) -> Text:
        prefix = Text(" " * self.content_padding)

        if emoji:
            prefix.append_text(Text.from_markup(emoji))

        prefix.pad_right(
            self.content_padding + self.emoji_column_width - prefix.cell_len
        )

        return prefix


LOG_LEVEL_COLORS = {
    "debug": "blue",
    "info": "cyan",
    "warning": "yellow",
    "warn": "yellow",
    "error": "red",
    "critical": "magenta",
    "fatal": "magenta",
}


def _get_log_bullet(level: str) -> str:
    """Colored bar rendered in the emoji bullet column, matching the log
    level, like the ``fastapi cloud logs`` output."""
    color = LOG_LEVEL_COLORS.get(level.lower(), "dim")

    return f"[{color}]▕[/{color}]"


class CustomFormatter(DefaultFormatter):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.toolkit = get_rich_toolkit()

    def formatMessage(self, record: logging.LogRecord) -> str:
        message = record.getMessage()
        result = self.toolkit.print_as_string(
            message, emoji=_get_log_bullet(record.levelname)
        )
        # Prepend newline to fix alignment after ^C is printed by the terminal
        if message == "Shutting down":
            result = "\n" + result
        return result


def get_uvicorn_log_config() -> dict[str, Any]:
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": CustomFormatter,
                "fmt": "%(levelprefix)s %(message)s",
                "use_colors": None,
            },
            "access": {
                "()": CustomFormatter,
                "fmt": "%(levelprefix)s %(client_addr)s - '%(request_line)s' %(status_code)s",
            },
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
            },
            "access": {
                "formatter": "access",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "uvicorn": {
                "handlers": ["default"],
                "level": "INFO",
                "propagate": False,
            },
            "uvicorn.error": {"level": "INFO"},
            "uvicorn.access": {
                "handlers": ["access"],
                "level": "INFO",
                "propagate": False,
            },
        },
    }


def get_rich_toolkit() -> RichToolkit:
    return RichToolkit(style=FastAPIStyle())
