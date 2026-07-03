import io
import logging
import sys
from logging.config import dictConfig

from pytest import LogCaptureFixture, MonkeyPatch

from fastapi_cli.utils.cli import (
    CustomFormatter,
    FastAPIStyle,
    MinimalEmojiStyle,
    get_rich_toolkit,
    get_uvicorn_log_config,
    should_use_rich_logs,
)


def test_get_uvicorn_config_uses_custom_formatter() -> None:
    config = get_uvicorn_log_config()

    assert config["formatters"]["default"]["()"] is CustomFormatter
    assert config["formatters"]["access"]["()"] is CustomFormatter
    assert config["loggers"]["uvicorn"]["propagate"] is False


def test_should_use_rich_logs_is_false_without_tty(
    monkeypatch: MonkeyPatch,
) -> None:
    monkeypatch.setattr(sys, "stdout", io.StringIO())

    assert should_use_rich_logs() is False


def test_get_rich_toolkit_uses_fastapi_style_when_requested() -> None:
    toolkit = get_rich_toolkit(use_rich=True)

    assert isinstance(toolkit.style, FastAPIStyle)


def test_get_rich_toolkit_uses_minimal_style_without_rich() -> None:
    toolkit = get_rich_toolkit(use_rich=False)

    assert isinstance(toolkit.style, MinimalEmojiStyle)


def test_get_rich_toolkit_uses_minimal_style_without_tty(
    monkeypatch: MonkeyPatch,
) -> None:
    monkeypatch.setattr(sys, "stdout", io.StringIO())

    toolkit = get_rich_toolkit(use_rich=should_use_rich_logs())

    assert isinstance(toolkit.style, MinimalEmojiStyle)


def test_custom_formatter() -> None:
    formatter = CustomFormatter()

    record = logging.LogRecord(
        name="uvicorn.access",
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg="%(client_addr)s - '%(request_line)s' %(status_code)s",
        args={
            "client_addr": "127.0.0.1",
            "request_line": "GET / HTTP/1.1",
            "status_code": 200,
        },
        exc_info=None,
    )

    formatted = formatter.formatMessage(record)

    # the log level is shown as a colored bar bullet, like `fastapi cloud logs`
    assert "▕" in formatted
    assert "127.0.0.1" in formatted
    assert "GET / HTTP/1.1" in formatted
    assert "200" in formatted


def test_custom_formatter_shutdown_prepends_newline() -> None:
    formatter = CustomFormatter()

    record = logging.LogRecord(
        name="uvicorn.error",
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg="Shutting down",
        args=(),
        exc_info=None,
    )

    formatted = formatter.formatMessage(record)

    assert formatted.startswith("\n")
    assert "Shutting down" in formatted


def test_log_config_does_not_disable_existing_loggers(
    caplog: LogCaptureFixture,
) -> None:
    logger1 = logging.getLogger(__name__)
    logger1.setLevel(logging.INFO)
    logger1.info("Message before configuration")

    dictConfig(get_uvicorn_log_config())

    logger2 = logging.getLogger(__name__)

    logger1.info("Message after configuration from logger1")  # Should not appear
    logger2.info("Message from logger2")

    assert "Message before configuration" in caplog.text
    assert "Message after configuration from logger1" in caplog.text
    assert "Message from logger2" in caplog.text
