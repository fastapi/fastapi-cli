import logging

from pytest import LogCaptureFixture

from fastapi_cli.utils.cli import CustomFormatter, get_uvicorn_log_config


def test_get_uvicorn_config_uses_custom_formatter() -> None:
    config = get_uvicorn_log_config()

    assert config["formatters"]["default"]["()"] is CustomFormatter
    assert config["formatters"]["access"]["()"] is CustomFormatter


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

    assert "INFO" in formatted
    assert "127.0.0.1" in formatted
    assert "GET / HTTP/1.1" in formatted
    assert "200" in formatted


def test_log_config_does_not_disable_existing_loggers(
    caplog: LogCaptureFixture,
) -> None:
    logger1 = logging.getLogger(__name__)
    logger1.setLevel(logging.INFO)
    logger1.info("Message before configuration")

    logging.config.dictConfig(get_uvicorn_log_config())

    logger2 = logging.getLogger(__name__)

    logger1.info("Message after configuration from logger1")  # Should not appear
    logger2.info("Message from logger2")

    assert "Message before configuration" in caplog.text
    assert "Message after configuration from logger1" in caplog.text
    assert "Message from logger2" in caplog.text
