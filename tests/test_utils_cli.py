import logging

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
