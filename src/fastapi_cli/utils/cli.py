import logging
import os
import sys
import time
from collections.abc import Iterator
from typing import Any, cast

from rich._loop import loop_first_last
from rich.console import Console, ConsoleOptions, Group, RenderableType, RenderResult
from rich.padding import Padding
from rich.segment import Segment
from rich.style import Style
from rich.text import Text
from rich_toolkit import RichToolkit, RichToolkitTheme
from rich_toolkit.container import Container
from rich_toolkit.element import CursorOffset, Element
from rich_toolkit.input import Input
from rich_toolkit.progress import Progress
from rich_toolkit.styles import BaseStyle, TaggedStyle
from uvicorn.logging import DefaultFormatter

logger = logging.getLogger(__name__)


# the leading space right-aligns the one-cell ✗ within the two-cell emoji
# slot, so its right edge and gap to the text match the emoji bullets
ERROR_BULLET = " [bold][error]✗[/][/]"


TITLE_SWEEP_SHADES = ("█", "▓", "▓", "▒", "░")
TITLE_SWEEP_DELAY = 0.015


def is_ci_enabled() -> bool:
    value = os.environ.get("CI")

    if value is None:
        return False

    return value.lower() not in {"", "0", "false", "no", "off"}


def should_use_rich_logs() -> bool:
    """Return True when stdout is a TTY and rich logs should be used, False otherwise."""
    return sys.stdout.isatty()


def _title_sweep_frames(text: str) -> Iterator[tuple[str, str, str]]:
    """Frames of a gradient sweep painting the title chip into existence.

    Each frame is split into the part of the chip already swept (rendered
    with the chip's background), the visible sweep shades, and the still
    untouched tail, all together exactly as wide as the chip (one space of
    padding around the text) so the real chip prints cleanly over the last
    frame."""
    chip = f" {text} "
    width = len(chip)

    for light_pos in range(-len(TITLE_SWEEP_SHADES), width + len(TITLE_SWEEP_SHADES)):
        sweep_start = light_pos - len(TITLE_SWEEP_SHADES) + 1
        chip_end = max(0, min(width, sweep_start))

        shades = "".join(
            shade
            for index, shade in enumerate(TITLE_SWEEP_SHADES)
            if 0 <= sweep_start + index < width
        )
        tail = " " * (width - chip_end - len(shades))

        yield chip[:chip_end], shades, tail


class IndentedBlock:
    """Indent a renderable, hanging a prefix (e.g. an emoji bullet) on the
    first line.

    Blank lines stay truly empty: live renders (inputs, menus) don't end
    with a newline, so any padding on a final blank line would leave the
    terminal cursor mid-line and shift whatever gets printed next.
    """

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

        for first, last, line in loop_first_last(lines):
            if any(segment.text.strip() for segment in line):
                yield from console.render(
                    self.first_prefix if first else self.prefix, options
                )
                yield from line
            elif last:
                # a zero-width space stops live renders from stripping the
                # final blank line, keeping the cursor at column 0
                yield Segment("​")

            yield new_line


class FastAPIStyle(BaseStyle):
    """Header chip + uniform indent, without the per-line tag gutter.

    Titles render as a single chip at the top of the command's output and
    everything else gets a fixed left indent, so renderables don't need to
    be wrapped in `Padding` manually. Emojis (`emoji=` metadata, or the
    progress animation/done emoji) hang to the left of the text like list
    bullets.

    This is the shared style used by both fastapi-cli and fastapi-cloud-cli.
    """

    content_padding = 1
    emoji_column_width = 3

    animation_emojis = [
        "🥚",
        "🐣",
        "🐤",
        "🐥",
        "🐓",
        "🐔",
    ]

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

        # progress log lines and container children are already part of
        # their parent's render, which gets indented as a whole
        if isinstance(parent, (Progress, Container)):
            return rendered

        metadata = kwargs
        if isinstance(element, Element) and element.metadata:
            metadata = {**element.metadata, **metadata}

        # Input.ask wraps the element in a metadata-less Container; pull the
        # child's metadata so flags like bullet= still apply
        if isinstance(element, Container) and element.elements:
            child = element.elements[0]
            if isinstance(child, Element) and child.metadata:
                metadata = {**child.metadata, **metadata}

        if metadata.get("title", False):
            return self._render_title(element, metadata)

        if isinstance(element, Progress):
            emoji = self._get_progress_status_emoji(element, done)
        else:
            emoji = metadata.get("emoji", "")

        if not emoji and not metadata.get("bullet", True):
            # skip the bullet column and align with the title chip's text
            indent = Text(" " * (self.title_padding + 1))
            return IndentedBlock(rendered, first_prefix=indent, prefix=indent)

        return self._render_with_emoji_bullet(rendered, emoji)

    @property
    def title_padding(self) -> int:
        # align the chip with the emoji bullet column
        return self.content_padding

    def _render_title(self, title: Any, metadata: dict[str, Any]) -> RenderableType:
        tag = metadata.get("tag", "")

        if metadata.get("animate", False):
            self._animate_title_sweep(tag or title)

        chip = Padding(
            Text(f" {tag or title} ", style="tag.title"),
            (0, 0, 0, self.title_padding),
            expand=False,
        )

        if not (tag and title):
            return chip

        title_text = self._render_with_emoji_bullet(
            Text.from_markup(f"[bold]{title}[/bold]"),
            metadata.get("emoji", ""),
        )

        return Group(chip, "", title_text)

    def _animate_title_sweep(self, text: str) -> None:
        """Sweep a gradient across the chip's line right before it prints,
        painting the chip background in behind the light."""
        if not self.console.is_terminal or is_ci_enabled():
            return

        indent = " " * self.title_padding
        # the shades sweep in the chip's background color over the bare
        # terminal, so the solid trailing edge blends into the painted chip
        sweep_style = Style(color=self.console.get_style("tag.title").bgcolor)

        self.console.show_cursor(False)
        try:
            for chip, shades, tail in _title_sweep_frames(text):
                self.console.print(
                    Text.assemble(
                        indent, (chip, "tag.title"), (shades, sweep_style), tail
                    ),
                    end="\r",
                )
                time.sleep(TITLE_SWEEP_DELAY)
        finally:
            self.console.show_cursor(True)

    def _get_progress_status_emoji(self, element: Progress, done: bool) -> str:
        if element._cancelled:
            return "🟡"

        if element.is_error:
            return ERROR_BULLET

        if done:
            return cast(str, element.metadata.get("done_emoji", "🐔"))

        if emoji := element.metadata.get("emoji"):
            return cast(str, emoji)

        return self.animation_emojis[
            self.animation_counter % len(self.animation_emojis)
        ]

    def _render_with_emoji_bullet(
        self, rendered: RenderableType, emoji: str
    ) -> RenderableType:
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

    def get_cursor_offset_for_element(
        self, element: Element, parent: Element | None = None
    ) -> CursorOffset:
        has_bullet_column = bool(element.metadata.get("emoji")) or element.metadata.get(
            "bullet", True
        )

        decoration_width = (
            self.content_padding + self.emoji_column_width
            if has_bullet_column
            else self.title_padding + 1
        )

        offset = element.cursor_offset
        top = offset.top
        left = decoration_width + offset.left

        if isinstance(element, Input) and not element.inline and element.label:
            label_lines = self._count_label_lines(
                element.label, decoration_width=decoration_width
            )
            top = label_lines + 1

        return CursorOffset(top=top, left=left)


class CustomFormatter(DefaultFormatter):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.toolkit = get_rich_toolkit()

    def formatMessage(self, record: logging.LogRecord) -> str:
        message = record.getMessage()
        result = self.toolkit.print_as_string(message, tag=record.levelname)
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
    theme = RichToolkitTheme(
        style=TaggedStyle(tag_width=11),
        theme={
            "tag.title": "white on #009485",
            "tag": "white on #007166",
            "placeholder": "grey85",
            "text": "white",
            "selected": "#007166",
            "result": "grey85",
            "progress": "on #007166",
            "error": "red",
            "log.info": "black on blue",
        },
    )

    return RichToolkit(theme=theme)
