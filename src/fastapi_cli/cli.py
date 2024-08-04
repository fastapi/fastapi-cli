import asyncio
from enum import Enum
from logging import getLogger
from pathlib import Path
from typing import Any, Literal, Optional, Union

import typer
from rich import print
from rich.padding import Padding
from rich.panel import Panel
from typing_extensions import Annotated

from fastapi_cli.discover import get_import_string
from fastapi_cli.exceptions import FastAPICLIException

from . import __version__
from .logging import setup_logging

app = typer.Typer(rich_markup_mode="rich")


class WSProtocolType(str, Enum):
    auto = "auto"
    none = "none"
    websockets = "websockets"
    wsproto = "wsproto"


setup_logging()
logger = getLogger(__name__)

try:
    import uvicorn
except ImportError:  # pragma: no cover
    uvicorn = None  # type: ignore[assignment]


def version_callback(value: bool) -> None:
    if value:
        print(f"FastAPI CLI version: [green]{__version__}[/green]")
        raise typer.Exit()


@app.callback()
def callback(
    version: Annotated[
        Union[bool, None],
        typer.Option(
            "--version", help="Show the version and exit.", callback=version_callback
        ),
    ] = None,
) -> None:
    """
    FastAPI CLI - The [bold]fastapi[/bold] command line app. 😎

    Manage your [bold]FastAPI[/bold] projects, run your FastAPI apps, and more.

    Read more in the docs: [link]https://fastapi.tiangolo.com/fastapi-cli/[/link].
    """


def _run(
    path: Union[Path, None] = None,
    *,
    host: str = "127.0.0.1",
    port: int = 8000,
    reload: bool = True,
    workers: Union[int, None] = None,
    root_path: str = "",
    command: str,
    app: Union[str, None] = None,
    proxy_headers: bool = False,
    ws: type[asyncio.Protocol] | WSProtocolType = "auto",
    ws_max_size: int = 16777216,
    ws_max_queue: int = 32,
    ws_ping_interval: Optional[float] = 20.0,
    ws_ping_timeout: Optional[float] = 20.0,
    ws_per_message_deflate: bool = True,
) -> None:
    try:
        use_uvicorn_app = get_import_string(path=path, app_name=app)
    except FastAPICLIException as e:
        logger.error(str(e))
        raise typer.Exit(code=1) from None
    serving_str = f"[dim]Serving at:[/dim] [link]http://{host}:{port}[/link]\n\n[dim]API docs:[/dim] [link]http://{host}:{port}/docs[/link]"

    if command == "dev":
        panel = Panel(
            f"{serving_str}\n\n[dim]Running in development mode, for production use:[/dim] \n\n[b]fastapi run[/b]",
            title="FastAPI CLI - Development mode",
            expand=False,
            padding=(1, 2),
            style="black on yellow",
        )
    else:
        panel = Panel(
            f"{serving_str}\n\n[dim]Running in production mode, for development use:[/dim] \n\n[b]fastapi dev[/b]",
            title="FastAPI CLI - Production mode",
            expand=False,
            padding=(1, 2),
            style="green",
        )
    print(Padding(panel, 1))
    if not uvicorn:
        raise FastAPICLIException(
            "Could not import Uvicorn, try running 'pip install uvicorn'"
        ) from None
    uvicorn.run(
        app=use_uvicorn_app,
        host=host,
        port=port,
        reload=reload,
        workers=workers,
        root_path=root_path,
        proxy_headers=proxy_headers,
        ws=ws,
        ws_max_size=ws_max_size,
        ws_max_queue=ws_max_queue,
        ws_ping_interval=ws_ping_interval,
        ws_ping_timeout=ws_ping_timeout,
        ws_per_message_deflate=ws_per_message_deflate,
    )


@app.command()
def dev(
    path: Annotated[
        Union[Path, None],
        typer.Argument(
            help="A path to a Python file or package directory (with [blue]__init__.py[/blue] files) containing a [bold]FastAPI[/bold] app. If not provided, a default set of paths will be tried."
        ),
    ] = None,
    *,
    host: Annotated[
        str,
        typer.Option(
            help="The host to serve on. For local development in localhost use [blue]127.0.0.1[/blue]. To enable public access, e.g. in a container, use all the IP addresses available with [blue]0.0.0.0[/blue]."
        ),
    ] = "127.0.0.1",
    port: Annotated[
        int,
        typer.Option(
            help="The port to serve on. You would normally have a termination proxy on top (another program) handling HTTPS on port [blue]443[/blue] and HTTP on port [blue]80[/blue], transferring the communication to your app."
        ),
    ] = 8000,
    reload: Annotated[
        bool,
        typer.Option(
            help="Enable auto-reload of the server when (code) files change. This is [bold]resource intensive[/bold], use it only during development."
        ),
    ] = True,
    root_path: Annotated[
        str,
        typer.Option(
            help="The root path is used to tell your app that it is being served to the outside world with some [bold]path prefix[/bold] set up in some termination proxy or similar."
        ),
    ] = "",
    app: Annotated[
        Union[str, None],
        typer.Option(
            help="The name of the variable that contains the [bold]FastAPI[/bold] app in the imported module or package. If not provided, it is detected automatically."
        ),
    ] = None,
    proxy_headers: Annotated[
        bool,
        typer.Option(
            help="Enable/Disable X-Forwarded-Proto, X-Forwarded-For, X-Forwarded-Port to populate remote address info."
        ),
    ] = True,
    ws: Annotated[
        WSProtocolType,
        typer.Option(
            help="The WebSocket protocol.", case_sensitive=False, show_choices=True
        ),
    ] = WSProtocolType.auto,
    ws_max_size: Annotated[
        int,
        typer.Option(help="WebSocket max size message in bytes."),
    ] = 16777216,
    ws_max_queue: Annotated[
        int,
        typer.Option(help="The maximum length of the WebSocket message queue."),
    ] = 32,
    ws_ping_interval: Annotated[
        Optional[float],
        typer.Option(help="WebSocket ping interval in seconds."),
    ] = 20.0,
    ws_ping_timeout: Annotated[
        Optional[float],
        typer.Option(help="WebSocket ping timeout in seconds."),
    ] = 20.0,
    ws_per_message_deflate: Annotated[
        bool,
        typer.Option(help="WebSocket per-message-deflate compression"),
    ] = True,
) -> Any:
    """
    Run a [bold]FastAPI[/bold] app in [yellow]development[/yellow] mode. 🧪

    This is equivalent to [bold]fastapi run[/bold] but with [bold]reload[/bold] enabled and listening on the [blue]127.0.0.1[/blue] address.

    It automatically detects the Python module or package that needs to be imported based on the file or directory path passed.

    If no path is passed, it tries with:

    - [blue]main.py[/blue]
    - [blue]app.py[/blue]
    - [blue]api.py[/blue]
    - [blue]app/main.py[/blue]
    - [blue]app/app.py[/blue]
    - [blue]app/api.py[/blue]

    It also detects the directory that needs to be added to the [bold]PYTHONPATH[/bold] to make the app importable and adds it.

    It detects the [bold]FastAPI[/bold] app object to use. By default it looks in the module or package for an object named:

    - [blue]app[/blue]
    - [blue]api[/blue]

    Otherwise, it uses the first [bold]FastAPI[/bold] app found in the imported module or package.
    """
    _run(
        path=path,
        host=host,
        port=port,
        reload=reload,
        root_path=root_path,
        app=app,
        command="dev",
        proxy_headers=proxy_headers,
        ws=ws,
        ws_max_size=ws_max_size,
        ws_max_queue=ws_max_queue,
        ws_ping_interval=ws_ping_interval,
        ws_ping_timeout=ws_ping_timeout,
        ws_per_message_deflate=ws_per_message_deflate,
    )


@app.command()
def run(
    path: Annotated[
        Union[Path, None],
        typer.Argument(
            help="A path to a Python file or package directory (with [blue]__init__.py[/blue] files) containing a [bold]FastAPI[/bold] app. If not provided, a default set of paths will be tried."
        ),
    ] = None,
    *,
    host: Annotated[
        str,
        typer.Option(
            help="The host to serve on. For local development in localhost use [blue]127.0.0.1[/blue]. To enable public access, e.g. in a container, use all the IP addresses available with [blue]0.0.0.0[/blue]."
        ),
    ] = "0.0.0.0",
    port: Annotated[
        int,
        typer.Option(
            help="The port to serve on. You would normally have a termination proxy on top (another program) handling HTTPS on port [blue]443[/blue] and HTTP on port [blue]80[/blue], transferring the communication to your app."
        ),
    ] = 8000,
    reload: Annotated[
        bool,
        typer.Option(
            help="Enable auto-reload of the server when (code) files change. This is [bold]resource intensive[/bold], use it only during development."
        ),
    ] = False,
    workers: Annotated[
        Union[int, None],
        typer.Option(
            help="Use multiple worker processes. Mutually exclusive with the --reload flag."
        ),
    ] = None,
    root_path: Annotated[
        str,
        typer.Option(
            help="The root path is used to tell your app that it is being served to the outside world with some [bold]path prefix[/bold] set up in some termination proxy or similar."
        ),
    ] = "",
    app: Annotated[
        Union[str, None],
        typer.Option(
            help="The name of the variable that contains the [bold]FastAPI[/bold] app in the imported module or package. If not provided, it is detected automatically."
        ),
    ] = None,
    proxy_headers: Annotated[
        bool,
        typer.Option(
            help="Enable/Disable X-Forwarded-Proto, X-Forwarded-For, X-Forwarded-Port to populate remote address info."
        ),
    ] = True,
    ws: Annotated[
        WSProtocolType,
        typer.Option(
            help="The WebSocket protocol.", case_sensitive=False, show_choices=True
        ),
    ] = WSProtocolType.auto,
    ws_max_size: Annotated[
        int,
        typer.Option(help="WebSocket max size message in bytes."),
    ] = 16777216,
    ws_max_queue: Annotated[
        int,
        typer.Option(help="The maximum length of the WebSocket message queue."),
    ] = 32,
    ws_ping_interval: Annotated[
        Optional[float],
        typer.Option(help="WebSocket ping interval in seconds."),
    ] = 20.0,
    ws_ping_timeout: Annotated[
        Optional[float],
        typer.Option(help="WebSocket ping timeout in seconds."),
    ] = 20.0,
    ws_per_message_deflate: Annotated[
        bool,
        typer.Option(help="WebSocket per-message-deflate compression"),
    ] = True,
) -> Any:
    """
    Run a [bold]FastAPI[/bold] app in [green]production[/green] mode. 🚀

    This is equivalent to [bold]fastapi dev[/bold] but with [bold]reload[/bold] disabled and listening on the [blue]0.0.0.0[/blue] address.

    It automatically detects the Python module or package that needs to be imported based on the file or directory path passed.

    If no path is passed, it tries with:

    - [blue]main.py[/blue]
    - [blue]app.py[/blue]
    - [blue]api.py[/blue]
    - [blue]app/main.py[/blue]
    - [blue]app/app.py[/blue]
    - [blue]app/api.py[/blue]

    It also detects the directory that needs to be added to the [bold]PYTHONPATH[/bold] to make the app importable and adds it.

    It detects the [bold]FastAPI[/bold] app object to use. By default it looks in the module or package for an object named:

    - [blue]app[/blue]
    - [blue]api[/blue]

    Otherwise, it uses the first [bold]FastAPI[/bold] app found in the imported module or package.
    """
    _run(
        path=path,
        host=host,
        port=port,
        reload=reload,
        workers=workers,
        root_path=root_path,
        app=app,
        command="run",
        proxy_headers=proxy_headers,
        ws=ws,
        ws_max_size=ws_max_size,
        ws_max_queue=ws_max_queue,
        ws_ping_interval=ws_ping_interval,
        ws_ping_timeout=ws_ping_timeout,
        ws_per_message_deflate=ws_per_message_deflate,
    )


def main() -> None:
    app()
