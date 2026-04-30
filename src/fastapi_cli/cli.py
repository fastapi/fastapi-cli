import logging
from pathlib import Path
from typing import Annotated, Any

import typer
from pydantic import ValidationError
from rich import print
from rich.syntax import Syntax
from rich.tree import Tree

from fastapi_cli.config import FastAPIConfig
from fastapi_cli.discover import (
    AppConfigSource,
    ModuleConfigSource,
    get_import_data,
    get_import_data_from_import_string,
)
from fastapi_cli.exceptions import FastAPICLIException

from . import __version__
from .logging import setup_logging
from .utils.cli import get_rich_toolkit, get_uvicorn_log_config

app = typer.Typer(
    rich_markup_mode="rich", context_settings={"help_option_names": ["-h", "--help"]}
)

logger = logging.getLogger(__name__)


SOURCE_DESCRIPTIONS: dict[ModuleConfigSource | AppConfigSource, str] = {
    "entrypoint-option": "[blue]--entrypoint[/] CLI option",
    "entrypoint-pyproject": "[blue]entrypoint[/] in [blue]pyproject.toml[/]",
    "path-argument": "[blue]path[/] CLI argument",
    "app-option": "[blue]--app[/] CLI option",
    "auto-discovery": "auto-discovery",
}


try:
    import uvicorn
except ImportError:  # pragma: no cover
    uvicorn = None  # type: ignore[assignment]  # ty: ignore[invalid-assignment]


try:
    from fastapi_cloud_cli.cli import (
        app as fastapi_cloud_cli,
    )

    app.add_typer(fastapi_cloud_cli)
except ImportError:  # pragma: no cover
    pass


try:
    from fastapi_new.cli import (  # type: ignore[import-not-found]  # ty: ignore[unresolved-import]
        app as fastapi_new_cli,
    )

    app.add_typer(fastapi_new_cli)  # pragma: no cover
except ImportError:  # pragma: no cover
    pass


def version_callback(value: bool) -> None:
    if value:
        print(f"FastAPI CLI version: [green]{__version__}[/green]")
        raise typer.Exit()


@app.callback()
def callback(
    version: Annotated[
        bool | None,
        typer.Option(
            "--version", help="Show the version and exit.", callback=version_callback
        ),
    ] = None,
    verbose: bool = typer.Option(False, help="Enable verbose output"),
) -> None:
    """
    FastAPI CLI - The [bold]fastapi[/bold] command line app. 😎

    Manage your [bold]FastAPI[/bold] projects, run your FastAPI apps, and more.

    Read more in the docs: [link=https://fastapi.tiangolo.com/fastapi-cli/]https://fastapi.tiangolo.com/fastapi-cli/[/link].
    """

    log_level = logging.DEBUG if verbose else logging.INFO

    setup_logging(level=log_level)


def _get_module_tree(module_paths: list[Path]) -> Tree:
    root = module_paths[0]
    name = f"🐍 {root.name}" if root.is_file() else f"📁 {root.name}"

    root_tree = Tree(name)

    if root.is_dir():
        root_tree.add("[dim]🐍 __init__.py[/dim]")

    tree = root_tree
    for sub_path in module_paths[1:]:
        sub_name = (
            f"🐍 {sub_path.name}" if sub_path.is_file() else f"📁 {sub_path.name}"
        )
        tree = tree.add(sub_name)
        if sub_path.is_dir():
            tree.add("[dim]🐍 __init__.py[/dim]")

    return root_tree


def _run(
    path: Path | None = None,
    *,
    host: str = "127.0.0.1",
    port: int = 8000,
    reload: bool = True,
    reload_dirs: list[Path] | None = None,
    workers: int | None = None,
    root_path: str = "",
    command: str,
    app: str | None = None,
    entrypoint: str | None = None,
    proxy_headers: bool = False,
    forwarded_allow_ips: str | None = None,
) -> None:
    with get_rich_toolkit() as toolkit:
        server_type = "development" if command == "dev" else "production"

        toolkit.print_title(f"Starting {server_type} server 🚀", tag="FastAPI")
        toolkit.print_line()

        toolkit.print(
            "Searching for package file structure from directories with [blue]__init__.py[/blue] files"
        )

        if entrypoint and (path or app):
            toolkit.print_line()
            toolkit.print(
                "[error]Cannot use --entrypoint together with path or --app arguments"
            )
            toolkit.print_line()
            raise typer.Exit(code=1)

        try:
            config = FastAPIConfig.resolve(entrypoint=entrypoint)
        except ValidationError as e:
            toolkit.print_line()
            toolkit.print("[error]Invalid configuration in pyproject.toml:")
            toolkit.print_line()

            for error in e.errors():
                field = ".".join(str(loc) for loc in error["loc"])
                toolkit.print(f"  [red]•[/red] {field}: {error['msg']}")

            toolkit.print_line()

            raise typer.Exit(code=1) from None

        try:
            # Resolve import data with priority: CLI path/app > config entrypoint > auto-discovery
            if path or app:
                import_data = get_import_data(path=path, app_name=app)
            elif config.entrypoint:
                import_data = get_import_data_from_import_string(
                    config.entrypoint, config.from_pyproject
                )
            else:
                import_data = get_import_data()
        except FastAPICLIException as e:
            toolkit.print_line()
            toolkit.print(f"[error]{e}")
            raise typer.Exit(code=1) from None

        logger.debug(f"Importing from {import_data.module_data.extra_sys_path}")
        logger.debug(f"Importing module {import_data.module_data.module_import_str}")

        module_data = import_data.module_data
        import_string = import_data.import_string

        toolkit.print(f"Importing from {module_data.extra_sys_path}")
        toolkit.print_line()

        if module_data.module_paths:
            root_tree = _get_module_tree(module_data.module_paths)

            toolkit.print(root_tree, tag="module")
            toolkit.print_line()

        toolkit.print(
            "Importing the FastAPI app object from the module with the following code:",
            tag="code",
        )
        toolkit.print_line()
        toolkit.print(
            f"[underline]from [bold]{module_data.module_import_str}[/bold] import [bold]{import_data.app_name}[/bold]"
        )
        toolkit.print_line()

        toolkit.print(
            f"Using import string: [blue]{import_string}[/]",
            tag="app",
        )

        mod_source_desc = SOURCE_DESCRIPTIONS[import_data.module_config_source]
        app_source_desc = SOURCE_DESCRIPTIONS[import_data.app_name_config_source]
        toolkit.print_line()
        toolkit.print("Configuration sources:", tag="info")
        if mod_source_desc == app_source_desc:
            toolkit.print(f" • Import string: {mod_source_desc}")
        else:
            toolkit.print(f" • Module: {mod_source_desc}")
            toolkit.print(f" • App name: {app_source_desc}")

        if import_data.module_config_source == "auto-discovery":
            toolkit.print_line()
            toolkit.print(
                "You can configure an entrypoint in [blue]pyproject.toml[/] for this app with:",
                tag="tip",
            )
            toolkit.print_line()
            toolkit.print(
                Syntax(
                    (
                        "[tool.fastapi]\n"
                        f'entrypoint = "{import_data.module_data.module_import_str}:{import_data.app_name}"'
                    ),
                    "toml",
                    theme="ansi_light",
                )
            )

        url = f"http://{host}:{port}"
        url_docs = f"{url}/docs"

        toolkit.print_line()
        toolkit.print(
            f"Server started at [link={url}]{url}[/]",
            f"Documentation at [link={url_docs}]{url_docs}[/]",
            tag="server",
        )

        if command == "dev":
            toolkit.print_line()
            toolkit.print(
                "Running in development mode, for production use: [bold]fastapi run[/]",
                tag="tip",
            )

        if not uvicorn:
            raise FastAPICLIException(
                "Could not import Uvicorn, try running 'pip install uvicorn'"
            ) from None

        toolkit.print_line()
        toolkit.print("Logs:")
        toolkit.print_line()

        uvicorn.run(
            app=import_string,
            host=host,
            port=port,
            reload=reload,
            reload_dirs=(
                [str(directory.resolve()) for directory in reload_dirs]
                if reload_dirs
                else None
            ),
            workers=workers,
            root_path=root_path,
            proxy_headers=proxy_headers,
            forwarded_allow_ips=forwarded_allow_ips,
            log_config=get_uvicorn_log_config(),
        )


@app.command()
def dev(
    path: Annotated[
        Path | None,
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
            help="The port to serve on. You would normally have a termination proxy on top (another program) handling HTTPS on port [blue]443[/blue] and HTTP on port [blue]80[/blue], transferring the communication to your app.",
            envvar="PORT",
        ),
    ] = 8000,
    reload: Annotated[
        bool,
        typer.Option(
            help="Enable auto-reload of the server when (code) files change. This is [bold]resource intensive[/bold], use it only during development."
        ),
    ] = True,
    reload_dir: Annotated[
        list[Path] | None,
        typer.Option(
            help="Set reload directories explicitly, instead of using the current working directory."
        ),
    ] = None,
    root_path: Annotated[
        str,
        typer.Option(
            help="The root path is used to tell your app that it is being served to the outside world with some [bold]path prefix[/bold] set up in some termination proxy or similar."
        ),
    ] = "",
    app: Annotated[
        str | None,
        typer.Option(
            help="The name of the variable that contains the [bold]FastAPI[/bold] app in the imported module or package. If not provided, it is detected automatically."
        ),
    ] = None,
    entrypoint: Annotated[
        str | None,
        typer.Option(
            "--entrypoint",
            "-e",
            help="The FastAPI app import string in the format 'some.importable_module:app_name'.",
        ),
    ] = None,
    proxy_headers: Annotated[
        bool,
        typer.Option(
            help="Enable/Disable X-Forwarded-Proto, X-Forwarded-For, X-Forwarded-Port to populate remote address info."
        ),
    ] = True,
    forwarded_allow_ips: Annotated[
        str | None,
        typer.Option(
            help="Comma separated list of IP Addresses to trust with proxy headers. The literal '*' means trust everything."
        ),
    ] = None,
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
        reload_dirs=reload_dir,
        root_path=root_path,
        app=app,
        entrypoint=entrypoint,
        command="dev",
        proxy_headers=proxy_headers,
        forwarded_allow_ips=forwarded_allow_ips,
    )


@app.command()
def run(
    path: Annotated[
        Path | None,
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
            help="The port to serve on. You would normally have a termination proxy on top (another program) handling HTTPS on port [blue]443[/blue] and HTTP on port [blue]80[/blue], transferring the communication to your app.",
            envvar="PORT",
        ),
    ] = 8000,
    reload: Annotated[
        bool,
        typer.Option(
            help="Enable auto-reload of the server when (code) files change. This is [bold]resource intensive[/bold], use it only during development."
        ),
    ] = False,
    workers: Annotated[
        int | None,
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
        str | None,
        typer.Option(
            help="The name of the variable that contains the [bold]FastAPI[/bold] app in the imported module or package. If not provided, it is detected automatically."
        ),
    ] = None,
    entrypoint: Annotated[
        str | None,
        typer.Option(
            "--entrypoint",
            "-e",
            help="The FastAPI app import string in the format 'some.importable_module:app_name'.",
        ),
    ] = None,
    proxy_headers: Annotated[
        bool,
        typer.Option(
            help="Enable/Disable X-Forwarded-Proto, X-Forwarded-For, X-Forwarded-Port to populate remote address info."
        ),
    ] = True,
    forwarded_allow_ips: Annotated[
        str | None,
        typer.Option(
            help="Comma separated list of IP Addresses to trust with proxy headers. The literal '*' means trust everything."
        ),
    ] = None,
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
        entrypoint=entrypoint,
        command="run",
        proxy_headers=proxy_headers,
        forwarded_allow_ips=forwarded_allow_ips,
    )


def main() -> None:
    app()
