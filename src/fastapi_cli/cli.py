import os
from logging import getLogger
from pathlib import Path
from typing import Any, Dict, Union

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


def create_structure(structure: Dict[str, Any], base_path: str = ""):
    """
    Recursively creates a directory structure and files based on the provided dictionary.

    This function traverses a nested dictionary structure and creates corresponding
    directories and files. It can handle nested directories, empty files, and files with content.

    Args:
        structure (Dict[str, Any]): A dictionary representing the desired file/directory structure.
            - Keys are names of directories or files.
            - Values can be:
                - dict: represents a subdirectory
                - str: represents file content
                - list: represents a directory with multiple files or subdirectories
        base_path (str, optional): The base path where the structure should be created.
            Defaults to the current directory.

    Behavior:
        - If a value is a dict, it creates a directory and recursively calls itself.
        - If a value is a string, it creates a file with that content.
        - If a value is a list, it creates a directory and processes each item in the list:
            - String items become empty files.
            - Dict items are treated as {filename: content} pairs.

    Raises:
        OSError: If there's an issue creating directories or files.
        TypeError: If the structure contains unsupported types.

    Example:
        structure = {
            "dir1": {
                "file1.txt": "content",
                "subdir": {
                    "file2.txt": "more content"
                }
            },
            "dir2": [
                "empty_file.txt",
                {"config.json": '{"key": "value"}'}
            ]
        }
        create_structure(structure, "/path/to/base")

    Note:
        This function will overwrite existing files if they have the same name as items in the structure.
    """
    for key, value in structure.items():
        path = os.path.join(base_path, key)
        if isinstance(value, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(value, path)
        elif isinstance(value, str):
            with open(path, "w") as f:
                f.write(value)
        elif isinstance(value, list):
            os.makedirs(path, exist_ok=True)
            for item in value:
                if isinstance(item, str):
                    with open(os.path.join(path, item), "w") as f:
                        f.write("")
                elif isinstance(item, dict):
                    for file_name, content in item.items():
                        with open(os.path.join(path, file_name), "w") as f:
                            f.write(content)


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
    )


@app.command()
def init(name: str = typer.Option("fastapi_project", help="Name of the project")):
    """Initialize a new FastAPI project with example code"""
    project_structure = {
        name: {
            "app": {
                "api": {
                    "v1": {
                        "endpoints": [
                            {
                                "items.py": """from fastapi import APIRouter, HTTPException
from typing import List, Dict

router = APIRouter()

items = {}

@router.get("/items/", response_model=List[Dict[str, Any]])
async def read_items():
    return [{"id": k, **v} for k, v in items.items()]

@router.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]

@router.post("/items/")
async def create_item(item: Dict[str, Any]):
    item_id = max(items.keys() or [0]) + 1
    items[item_id] = item
    return {"id": item_id, **item}
"""
                            },
                            "__init__.py",
                        ],
                    },
                    "__init__.py": "",
                },
                "core": {
                    "config.py": """from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "FastAPI Project"
    debug: bool = False

    class Config:
        env_file = ".env"

settings = Settings()
""",
                    "__init__.py": "",
                },
                "db": {
                    "base.py": """from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
""",
                    "session.py": """from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
""",
                    "__init__.py": "",
                },
                "models": [
                    {
                        "item.py": """from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
"""
                    },
                    "__init__.py",
                ],
                "schemas": [
                    {
                        "item.py": """from pydantic import BaseModel

class ItemBase(BaseModel):
    title: str
    description: str = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True
"""
                    },
                    "__init__.py",
                ],
                "main.py": """from fastapi import FastAPI
from app.api.v1.endpoints import items
from app.core.config import settings

app = FastAPI(title=settings.app_name, debug=settings.debug)

app.include_router(items.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI!"}
""",
                "__init__.py": "",
            },
            "tests": [
                {
                    "test_main.py": """from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to FastAPI!"}
"""
                },
                "__init__.py",
            ],
            "requirements.txt": """fastapi==0.68.0
uvicorn==0.15.0
sqlalchemy==1.4.23
pydantic==1.8.2
""",
            "README.md": f"""# {name}

This is a FastAPI project generated using the FastAPI CLI tool.

## Getting Started

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the server:
   ```
   uvicorn app.main:app --reload
   ```

3. Open your browser and go to http://localhost:8000/docs to see the API documentation.

## Project Structure

- `app/`: Main application package
  - `api/`: API endpoints
  - `core/`: Core functionality (config, etc.)
  - `db/`: Database-related code
  - `models/`: SQLAlchemy models
  - `schemas/`: Pydantic schemas
  - `main.py`: Main FastAPI application
- `tests/`: Test files

## Running Tests

To run tests, use the following command:

```
pytest
```
""",
        }
    }

    create_structure(project_structure)
    typer.echo(f"FastAPI project '{name}' created successfully with example code!")


def main() -> None:
    app()
