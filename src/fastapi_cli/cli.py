from logging import getLogger
from typing import Union

import typer
from rich import print
from typing_extensions import Annotated

from fastapi_cli.commands import server  # noqa: F401

from . import __version__
from .app import app
from .logging import setup_logging


setup_logging()
logger = getLogger(__name__)


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


def main() -> None:
    app()
